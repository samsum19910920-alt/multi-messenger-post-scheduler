package com.example.messenger.scheduler.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

/**
 * جدول کاربران - ذخیره محلی اطلاعات کاربر
 */
@Entity(tableName = "users")
data class UserEntity(
    @PrimaryKey
    val id: Int,
    val phoneNumber: String,
    val isActive: Boolean,
    val subscriptionEnd: String?,
    val accessToken: String
)

/**
 * جدول کانال‌ها - ذخیره محلی کانال‌های کاربر
 */
@Entity(tableName = "channels")
data class ChannelEntity(
    @PrimaryKey
    val id: Int,
    val messengerType: String,
    val channelId: String,
    val channelName: String?,
    val channelUsername: String?,
    val isActive: Boolean,
    val createdAt: String
)

/**
 * جدول پست‌ها - ذخیره محلی پست‌های زمان‌بندی شده
 */
@Entity(tableName = "posts")
data class PostEntity(
    @PrimaryKey
    val id: Int,
    val caption: String?,
    val postType: String,
    val scheduledTime: String,
    val isSent: Boolean,
    val sentAt: String?,
    val createdAt: String
)
