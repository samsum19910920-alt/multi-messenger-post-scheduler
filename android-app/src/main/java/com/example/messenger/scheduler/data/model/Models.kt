package com.example.messenger.scheduler.data.model

import com.google.gson.annotations.SerializedName
from java.time.LocalDateTime

// Authentication Models
data class SendOtpRequest(
    @SerializedName("phone_number")
    val phoneNumber: String
)

data class VerifyOtpRequest(
    @SerializedName("phone_number")
    val phoneNumber: String,
    @SerializedName("otp_code")
    val otpCode: String,
    val password: String? = null
)

data class AuthResponse(
    @SerializedName("access_token")
    val accessToken: String,
    val user: User
)

data class User(
    val id: Int,
    @SerializedName("phone_number")
    val phoneNumber: String,
    @SerializedName("is_active")
    val isActive: Boolean,
    @SerializedName("subscription_end")
    val subscriptionEnd: String?
)

// Channel Models
data class AddChannelRequest(
    @SerializedName("messenger_type")
    val messengerType: String,
    @SerializedName("channel_id")
    val channelId: String,
    @SerializedName("channel_name")
    val channelName: String,
    @SerializedName("channel_username")
    val channelUsername: String,
    @SerializedName("bot_token")
    val botToken: String
)

data class Channel(
    val id: Int,
    @SerializedName("messenger_type")
    val messengerType: String,
    @SerializedName("channel_id")
    val channelId: String,
    @SerializedName("channel_name")
    val channelName: String?,
    @SerializedName("channel_username")
    val channelUsername: String?,
    @SerializedName("is_active")
    val isActive: Boolean,
    @SerializedName("created_at")
    val createdAt: String
)

data class ChannelsResponse(
    val channels: List<Channel>
)

// Post Models
data class CreatePostRequest(
    val caption: String,
    @SerializedName("scheduled_time")
    val scheduledTime: String,
    @SerializedName("post_type")
    val postType: String,
    @SerializedName("channel_ids")
    val channelIds: List<Int>
)

data class ScheduledPost(
    val id: Int,
    val caption: String?,
    @SerializedName("post_type")
    val postType: String,
    @SerializedName("scheduled_time")
    val scheduledTime: String,
    @SerializedName("is_sent")
    val isSent: Boolean,
    @SerializedName("sent_at")
    val sentAt: String?,
    @SerializedName("created_at")
    val createdAt: String
)

data class PostsResponse(
    val posts: List<ScheduledPost>
)

// Generic API Response
data class ApiResponse<T>(
    val data: T? = null,
    val error: String? = null,
    val message: String? = null
)
