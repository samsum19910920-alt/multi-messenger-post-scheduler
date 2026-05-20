package com.example.messenger.scheduler.data.local

import androidx.room.Database
import androidx.room.RoomDatabase
from com.example.messenger.scheduler.data.local.entity.*

/**
 * Room Database برای ذخیره محلی اطلاعات کاربر و کانال‌ها
 */
@Database(
    entities = [UserEntity::class, ChannelEntity::class, PostEntity::class],
    version = 1,
    exportSchema = false
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao
    abstract fun channelDao(): ChannelDao
    abstract fun postDao(): PostDao
}
