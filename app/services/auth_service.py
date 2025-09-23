import hashlib
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, create_refresh_token
from app.extensions import db
from app.models.user import User
from app.models.refresh_token import RefreshToken
from sqlalchemy.exc import IntegrityError

from flask_mail import Message
from flask import current_app, url_for
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from app.extensions import mail

class AuthService:
    @staticmethod
    def generate_reset_token(email):
        s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        return s.dumps(email, salt="password-reset-salt")

    @staticmethod
    def verify_reset_token(token, expiration=3600):
        s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        try:
            email = s.loads(token, salt="password-reset-salt", max_age=expiration)
        except (SignatureExpired, BadSignature):
            return None
        return email

    @staticmethod
    def send_reset_email(user, token):
        reset_url = url_for('auth.reset_password', token=token, _external=True)
        msg = Message(
            subject="Password Reset Request",
            recipients=[user.email],
            body=f"Hello {user.name},\n\nTo reset your password, click the following link (valid for 1 hour):\n{reset_url}\n\nIf you did not request this, please ignore this email."
        )
        mail.send(msg)

    @staticmethod
    def forgot_password(email):
        user = User.query.filter_by(email=email, is_active=True).first()
        if not user:
            raise ValueError("No user found with this email")
        token = AuthService.generate_reset_token(user.email)
        AuthService.send_reset_email(user, token)
        return True

    @staticmethod
    def reset_password(token, new_password):
        email = AuthService.verify_reset_token(token)
        if not email:
            raise ValueError("Invalid or expired token")
        user = User.query.filter_by(email=email, is_active=True).first()
        if not user:
            raise ValueError("User not found")
        user.set_password(new_password)
        RefreshToken.query.filter_by(user_id=user.id).delete()
        db.session.commit()
        return True
    
    @staticmethod
    def register_user(name, email, password):
        """Register a new user with User role by default"""
        try:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                raise ValueError("User with this email already exists")
            
            user = User(name=name, email=email, role='User')
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            return user
            
        except IntegrityError:
            db.session.rollback()
            raise ValueError("User with this email already exists")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Registration failed: {str(e)}")

    @staticmethod
    def authenticate(email, password):
        """Authenticate user by email and password"""
        user = User.query.filter_by(email=email, is_active=True).first()
        
        if not user or not user.check_password(password):
            raise ValueError("Invalid email or password")
        
        return user

    @staticmethod
    def create_tokens(user):
        """Create access and refresh tokens for user"""
        # FIXED: Convert user.id to string for JWT subject
        user_id_str = str(user.id)
        
        # Create JWT tokens
        access_token = create_access_token(
            identity=user_id_str,  # Must be string
            additional_claims={
                'role': user.role,
                'email': user.email,
                'name': user.name,
                'user_id': user.id  # Keep numeric ID in claims for convenience
            }
        )
        
        refresh_token = create_refresh_token(
            identity=user_id_str,  # Must be string
            additional_claims={
                'user_id': user.id
            }
        )
        
        # Store refresh token hash in database
        expires_at = datetime.utcnow() + timedelta(days=30)
        
        # Clean up old tokens for this user (keep only latest)
        RefreshToken.query.filter_by(user_id=user.id).delete()
        
        # Use the hash approach if using the RefreshToken with token_hash field
        if hasattr(RefreshToken, 'hash_token'):
            token_hash = RefreshToken.hash_token(refresh_token)
            refresh_token_obj = RefreshToken(
                token_hash=token_hash,
                user_id=user.id,
                expires_at=expires_at
            )
        else:
            # Use direct token storage (make sure your model supports this)
            refresh_token_obj = RefreshToken(
                token=refresh_token,
                user_id=user.id,
                expires_at=expires_at
            )
        
        db.session.add(refresh_token_obj)
        db.session.commit()
        
        return access_token, refresh_token

    @staticmethod
    def refresh_access_token(user_id_str):
        """Create new access token from refresh token"""
        # FIXED: Convert string back to int for database query
        user_id = int(user_id_str) if isinstance(user_id_str, str) else user_id_str
        
        user = User.query.filter_by(id=user_id, is_active=True).first()
        if not user:
            raise ValueError("User not found")
        
        access_token = create_access_token(
            identity=str(user.id),  # Must be string
            additional_claims={
                'role': user.role,
                'email': user.email,
                'name': user.name,
                'user_id': user.id
            }
        )
        
        return access_token

    @staticmethod
    def revoke_refresh_token(token):
        """Revoke a refresh token"""
        if hasattr(RefreshToken, 'hash_token'):
            token_hash = RefreshToken.hash_token(token)
            refresh_token = RefreshToken.query.filter_by(token_hash=token_hash).first()
        else:
            refresh_token = RefreshToken.query.filter_by(token=token).first()
            
        if refresh_token:
            if hasattr(refresh_token, 'revoke'):
                refresh_token.revoke()
            else:
                db.session.delete(refresh_token)
            db.session.commit()
            return True
        return False

    @staticmethod
    def change_password(user_id_str, current_password, new_password):
        """Change user password and revoke all refresh tokens. Admin can also change password."""
        user_id = int(user_id_str) if isinstance(user_id_str, str) else user_id_str
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        # Always require current password for security, even for admin
        if not user.check_password(current_password):
            raise ValueError("Current password is incorrect")
        user.set_password(new_password)
        RefreshToken.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        return True

    @staticmethod
    def create_admin_user(name="Admin", email="admin@gmail.com", password="123456"):
        """Create admin user if it doesn't exist"""
        try:
            admin = User.query.filter_by(email=email).first()
            if not admin:
                admin = User(name=name, email=email, role='Admin')
                admin.set_password(password)
                db.session.add(admin)
                db.session.commit()
                print(f"✅ Admin user created: {email}")
            else:
                print(f"ℹ️ Admin user already exists: {email}")
            return admin
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creating admin user: {e}")
            return None