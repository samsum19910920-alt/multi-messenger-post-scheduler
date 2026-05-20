# Multi-Messenger Post Scheduler API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication
All requests (except OTP endpoints) require a JWT token in the Authorization header:
```
Authorization: Bearer <JWT_TOKEN>
```

## Endpoints

### Authentication

#### Send OTP
```
POST /auth/send-otp
Content-Type: application/json

{
  "phone_number": "09xxxxxxxxx"
}
```

#### Verify OTP
```
POST /auth/verify-otp
Content-Type: application/json

{
  "phone_number": "09xxxxxxxxx",
  "otp_code": "123456",
  "password": "password123"  // For new users
}
```

### User

#### Get Profile
```
GET /user/profile
```

#### Get Subscription Status
```
GET /user/subscription-status
```

### Channels

#### Get All Channels
```
GET /channels/
```

#### Add Channel
```
POST /channels/
Content-Type: application/json

{
  "messenger_type": "bale",
  "channel_id": "channel_id",
  "channel_name": "Channel Name",
  "channel_username": "@channelname",
  "bot_token": "bot_token"
}
```

#### Delete Channel
```
DELETE /channels/<channel_id>
```

### Posts

#### Get All Posts
```
GET /posts/
```

#### Create Post
```
POST /posts/
Content-Type: multipart/form-data

Parameters:
- caption: Post caption (optional)
- scheduled_time: ISO 8601 format (required)
- post_type: text/image/video/mixed (required)
- files: Media files (optional)
```

#### Delete Post
```
DELETE /posts/<post_id>
```

### Admin

#### Get All Users
```
GET /admin/users
X-Admin-Key: <admin_key>
```

#### Delete User
```
DELETE /admin/users/<user_id>
X-Admin-Key: <admin_key>
```

#### Update Subscription
```
POST /admin/users/<user_id>/subscription
X-Admin-Key: <admin_key>
Content-Type: application/json

{
  "subscription_end": "2025-12-31T23:59:59"
}
```

#### Get Statistics
```
GET /admin/statistics
X-Admin-Key: <admin_key>
```
