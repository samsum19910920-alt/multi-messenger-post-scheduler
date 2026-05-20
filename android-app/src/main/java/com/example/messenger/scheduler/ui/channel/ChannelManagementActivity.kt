package com.example.messenger.scheduler.ui.channel

import android.os.Bundle
import android.widget.ArrayAdapter
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.example.messenger.scheduler.databinding.ActivityChannelManagementBinding
import com.example.messenger.scheduler.data.model.AddChannelRequest
import com.example.messenger.scheduler.data.repository.AppRepository
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.launch
import javax.inject.Inject

/**
 * صفحه مدیریت کانال‌ها - اضافه کردن و حذف کانال‌ها
 */
@AndroidEntryPoint
class ChannelManagementActivity : AppCompatActivity() {

    private lateinit var binding: ActivityChannelManagementBinding

    @Inject
    lateinit var repository: AppRepository

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityChannelManagementBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupMessengerSpinner()
        setupListeners()
        loadChannels()
    }

    private fun setupMessengerSpinner() {
        val messengers = arrayOf("Rubika", "Bale", "Eitaa", "Soroosh")
        val adapter = ArrayAdapter(this, android.R.layout.simple_spinner_dropdown_item, messengers)
        binding.spinnerMessenger.adapter = adapter
    }

    private fun setupListeners() {
        binding.btnAddChannel.setOnClickListener {
            val messengerType = binding.spinnerMessenger.selectedItem.toString().lowercase()
            val channelId = binding.etChannelId.text.toString()
            val botToken = binding.etBotToken.text.toString()

            if (channelId.isNotEmpty() && botToken.isNotEmpty()) {
                addChannel(messengerType, channelId, botToken)
            }
        }
    }

    private fun addChannel(messengerType: String, channelId: String, botToken: String) {
        lifecycleScope.launch {
            val request = AddChannelRequest(
                messengerType = messengerType,
                channelId = channelId,
                channelName = channelId,
                channelUsername = channelId,
                botToken = botToken
            )

            val result = repository.addChannel(request)
            result.onSuccess {
                binding.etChannelId.text?.clear()
                binding.etBotToken.text?.clear()
                loadChannels()
            }
        }
    }

    private fun loadChannels() {
        lifecycleScope.launch {
            val result = repository.getChannels()
            result.onSuccess { channels ->
                binding.tvChannelList.text = channels.joinToString("\n") { 
                    "${it.messengerType}: ${it.channelName}"
                }
            }
        }
    }
}
