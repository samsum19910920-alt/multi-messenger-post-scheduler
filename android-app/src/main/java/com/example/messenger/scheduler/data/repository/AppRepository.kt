package com.example.messenger.scheduler.data.repository

import com.example.messenger.scheduler.data.api.ApiService
import com.example.messenger.scheduler.data.local.AppDatabase
import com.example.messenger.scheduler.data.model.*
import com.example.messenger.scheduler.utils.PreferencesHelper
import javax.inject.Inject

/**
 * Repository برای مدیریت تمام درخواست‌های API و داده‌های محلی
 */
class AppRepository @Inject constructor(
    private val apiService: ApiService,
    private val database: AppDatabase,
    private val preferencesHelper: PreferencesHelper
) {

    // Authentication
    suspend fun sendOtp(phoneNumber: String): Result<Unit> = try {
        val response = apiService.sendOtp(SendOtpRequest(phoneNumber))
        if (response.error == null) Result.success(Unit)
        else Result.failure(Exception(response.error))
    } catch (e: Exception) {
        Result.failure(e)
    }

    suspend fun verifyOtp(phoneNumber: String, otpCode: String, password: String?): Result<AuthResponse> = try {
        val response = apiService.verifyOtp(VerifyOtpRequest(phoneNumber, otpCode, password))
        response.data?.let {
            preferencesHelper.saveToken(it.accessToken)
            preferencesHelper.saveUser(it.user)
            Result.success(it)
        } ?: Result.failure(Exception(response.error))
    } catch (e: Exception) {
        Result.failure(e)
    }

    // Channels
    suspend fun getChannels(): Result<List<Channel>> = try {
        val token = preferencesHelper.getToken() ?: return Result.failure(Exception("No token"))
        val response = apiService.getChannels("Bearer $token")
        response.data?.channels?.let {
            Result.success(it)
        } ?: Result.failure(Exception(response.error))
    } catch (e: Exception) {
        Result.failure(e)
    }

    suspend fun addChannel(request: AddChannelRequest): Result<Channel> = try {
        val token = preferencesHelper.getToken() ?: return Result.failure(Exception("No token"))
        val response = apiService.addChannel("Bearer $token", request)
        response.data?.let {
            Result.success(it)
        } ?: Result.failure(Exception(response.error))
    } catch (e: Exception) {
        Result.failure(e)
    }

    suspend fun deleteChannel(channelId: Int): Result<Unit> = try {
        val token = preferencesHelper.getToken() ?: return Result.failure(Exception("No token"))
        val response = apiService.deleteChannel("Bearer $token", channelId)
        if (response.error == null) Result.success(Unit)
        else Result.failure(Exception(response.error))
    } catch (e: Exception) {
        Result.failure(e)
    }

    // Posts
    suspend fun getPosts(): Result<List<ScheduledPost>> = try {
        val token = preferencesHelper.getToken() ?: return Result.failure(Exception("No token"))
        val response = apiService.getPosts("Bearer $token")
        response.data?.posts?.let {
            Result.success(it)
        } ?: Result.failure(Exception(response.error))
    } catch (e: Exception) {
        Result.failure(e)
    }

    suspend fun deletePost(postId: Int): Result<Unit> = try {
        val token = preferencesHelper.getToken() ?: return Result.failure(Exception("No token"))
        val response = apiService.deletePost("Bearer $token", postId)
        if (response.error == null) Result.success(Unit)
        else Result.failure(Exception(response.error))
    } catch (e: Exception) {
        Result.failure(e)
    }
}
