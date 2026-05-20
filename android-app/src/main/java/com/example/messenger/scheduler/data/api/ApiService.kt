package com.example.messenger.scheduler.data.api

import com.example.messenger.scheduler.data.model.*
import retrofit2.http.*

/**
 * Retrofit API Service برای ارتباط با Backend
 */
interface ApiService {

    // Authentication
    @POST("/api/auth/send-otp")
    suspend fun sendOtp(@Body request: SendOtpRequest): ApiResponse<Unit>

    @POST("/api/auth/verify-otp")
    suspend fun verifyOtp(@Body request: VerifyOtpRequest): ApiResponse<AuthResponse>

    @GET("/api/auth/me")
    suspend fun getCurrentUser(@Header("Authorization") token: String): ApiResponse<User>

    // Channels
    @GET("/api/channels/")
    suspend fun getChannels(@Header("Authorization") token: String): ApiResponse<ChannelsResponse>

    @POST("/api/channels/")
    suspend fun addChannel(
        @Header("Authorization") token: String,
        @Body request: AddChannelRequest
    ): ApiResponse<Channel>

    @DELETE("/api/channels/{id}")
    suspend fun deleteChannel(
        @Header("Authorization") token: String,
        @Path("id") channelId: Int
    ): ApiResponse<Unit>

    // Posts
    @GET("/api/posts/")
    suspend fun getPosts(@Header("Authorization") token: String): ApiResponse<PostsResponse>

    @Multipart
    @POST("/api/posts/")
    suspend fun createPost(
        @Header("Authorization") token: String,
        @Part("caption") caption: String,
        @Part("scheduled_time") scheduledTime: String,
        @Part("post_type") postType: String
    ): ApiResponse<ScheduledPost>

    @DELETE("/api/posts/{id}")
    suspend fun deletePost(
        @Header("Authorization") token: String,
        @Path("id") postId: Int
    ): ApiResponse<Unit>
}
