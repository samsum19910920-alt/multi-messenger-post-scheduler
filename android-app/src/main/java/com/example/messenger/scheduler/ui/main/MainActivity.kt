package com.example.messenger.scheduler.ui.main

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.example.messenger.scheduler.databinding.ActivityMainBinding
import com.example.messenger.scheduler.data.repository.AppRepository
import com.example.messenger.scheduler.ui.channel.ChannelManagementActivity
import com.example.messenger.scheduler.ui.post.CreatePostActivity
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.launch
import javax.inject.Inject

/**
 * صفحه اصلی - نمایش کانال‌ها و پست‌های زمان‌بندی شده
 */
@AndroidEntryPoint
class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding

    @Inject
    lateinit var repository: AppRepository

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupListeners()
        loadData()
    }

    private fun setupListeners() {
        binding.btnAddChannel.setOnClickListener {
            startActivity(Intent(this, ChannelManagementActivity::class.java))
        }

        binding.btnCreatePost.setOnClickListener {
            startActivity(Intent(this, CreatePostActivity::class.java))
        }
    }

    private fun loadData() {
        lifecycleScope.launch {
            // Load channels
            val channelsResult = repository.getChannels()
            channelsResult.onSuccess { channels ->
                binding.tvChannelCount.text = "کانال‌ها: ${channels.size}"
            }

            // Load posts
            val postsResult = repository.getPosts()
            postsResult.onSuccess { posts ->
                binding.tvPostCount.text = "پست‌ها: ${posts.size}"
            }
        }
    }
}
