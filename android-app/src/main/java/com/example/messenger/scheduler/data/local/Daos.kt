package com.example.messenger.scheduler.data.local

import androidx.room.*
from com.example.messenger.scheduler.data.local.entity.*

/**
 * Data Access Object برای جدول کاربران
 */
@Dao
interface UserDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertUser(user: UserEntity)

    @Query("SELECT * FROM users WHERE id = :userId")
    suspend fun getUser(userId: Int): UserEntity?

    @Query("DELETE FROM users")
    suspend fun clearAllUsers()
}

/**
 * Data Access Object برای جدول کانال‌ها
 */
@Dao
interface ChannelDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertChannels(channels: List<ChannelEntity>)

    @Query("SELECT * FROM channels")
    suspend fun getAllChannels(): List<ChannelEntity>

    @Query("DELETE FROM channels WHERE id = :channelId")
    suspend fun deleteChannel(channelId: Int)

    @Query("DELETE FROM channels")
    suspend fun clearAllChannels()
}

/**
 * Data Access Object برای جدول پست‌ها
 */
@Dao
interface PostDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertPosts(posts: List<PostEntity>)

    @Query("SELECT * FROM posts WHERE isSent = 0 ORDER BY scheduledTime ASC")
    suspend fun getPendingPosts(): List<PostEntity>

    @Query("DELETE FROM posts WHERE id = :postId")
    suspend fun deletePost(postId: Int)

    @Query("DELETE FROM posts")
    suspend fun clearAllPosts()
}
