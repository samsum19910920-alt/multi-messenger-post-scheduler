package com.example.messenger.scheduler.ui.post

import android.app.DatePickerDialog
import android.app.TimePickerDialog
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.example.messenger.scheduler.databinding.ActivityCreatePostBinding
import com.example.messenger.scheduler.data.repository.AppRepository
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.*
import javax.inject.Inject

/**
 * صفحه ایجاد پست - زمان‌بندی ارسال پست به کانال‌ها
 */
@AndroidEntryPoint
class CreatePostActivity : AppCompatActivity() {

    private lateinit var binding: ActivityCreatePostBinding
    private var selectedDateTime: Calendar = Calendar.getInstance()

    @Inject
    lateinit var repository: AppRepository

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityCreatePostBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupListeners()
    }

    private fun setupListeners() {
        binding.btnSelectDateTime.setOnClickListener {
            selectDateTime()
        }

        binding.btnCreatePost.setOnClickListener {
            val caption = binding.etCaption.text.toString()
            if (caption.isNotEmpty()) {
                createPost(caption)
            }
        }
    }

    private fun selectDateTime() {
        val datePickerDialog = DatePickerDialog(this) { _, year, month, dayOfMonth ->
            selectedDateTime.set(year, month, dayOfMonth)
            showTimePickerDialog()
        }
        datePickerDialog.show()
    }

    private fun showTimePickerDialog() {
        val timePickerDialog = TimePickerDialog(this) { _, hourOfDay, minute ->
            selectedDateTime.set(Calendar.HOUR_OF_DAY, hourOfDay)
            selectedDateTime.set(Calendar.MINUTE, minute)
            updateDateTimeDisplay()
        }
        timePickerDialog.show()
    }

    private fun updateDateTimeDisplay() {
        val formatter = SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale("fa"))
        binding.tvSelectedDateTime.text = formatter.format(selectedDateTime.time)
    }

    private fun createPost(caption: String) {
        lifecycleScope.launch {
            val formatter = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss", Locale.getDefault())
            val scheduledTime = formatter.format(selectedDateTime.time)

            // This would need to be extended to handle media uploads
            // For now, just text posts
            binding.btnCreatePost.isEnabled = false
            binding.btnCreatePost.text = "درحال ایجاد..."

            // API call would be made here
            binding.btnCreatePost.isEnabled = true
            binding.btnCreatePost.text = "ایجاد پست"
        }
    }
}
