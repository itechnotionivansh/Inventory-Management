
# app/models/refresh_token.py - FIXED VERSION
from datetime import datetime, timedelta
from app.extensions import db

class RefreshToken(db.Model):
    __tablename__ = "refresh_tokens"

    id = db.Column(db.Integer, primary_key=True)
    # FIXED: Use VARCHAR with specific length instead of TEXT for unique constraint
    token = db.Column(db.String(500), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_revoked = db.Column(db.Boolean, default=False)

    # Relationships
    user = db.relationship('User', backref=db.backref('refresh_tokens', lazy='dynamic'))

    @property
    def is_expired(self):
        return datetime.utcnow() > self.expires_at

    @property
    def is_valid(self):
        return not self.is_revoked and not self.is_expired

    def revoke(self):
        self.is_revoked = True

    def __repr__(self):
        return f"<RefreshToken user_id={self.user_id}>"