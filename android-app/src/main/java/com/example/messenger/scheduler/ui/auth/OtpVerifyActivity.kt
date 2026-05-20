package com.example.messenger.scheduler.ui.auth

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.example.messenger.scheduler.databinding.ActivityOtpVerifyBinding
import com.example.messenger.scheduler.data.repository.AppRepository
import com.example.messenger.scheduler.ui.main.MainActivity
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.launch
import javax.inject.Inject

/**
 * صفحه تایید OTP - دریافت کد OTP و رمز عبور (برای کاربران جدید)
 */
@AndroidEntryPoint
class OtpVerifyActivity : AppCompatActivity() {

    private lateinit var binding: ActivityOtpVerifyBinding
    private lateinit var phoneNumber: String

    @Inject
    lateinit var repository: AppRepository

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityOtpVerifyBinding.inflate(layoutInflater)
        setContentView(binding.root)

        phoneNumber = intent.getStringExtra("phone_number") ?: ""
        binding.tvPhoneNumber.text = "تایید OTP برای: $phoneNumber"

        setupListeners()
    }

    private fun setupListeners() {
        binding.btnVerifyOtp.setOnClickListener {
            val otpCode = binding.etOtpCode.text.toString()
            val password = binding.etPassword.text.toString()

            if (otpCode.isEmpty() || password.isEmpty()) {
                binding.tilOtpCode.error = "تمام فیلدها الزامی هستند"
                return@setOnClickListener
            }

            verifyOtp(otpCode, password)
        }
    }

    private fun verifyOtp(otpCode: String, password: String) {
        lifecycleScope.launch {
            binding.btnVerifyOtp.isEnabled = false

            val result = repository.verifyOtp(phoneNumber, otpCode, password)

            result.onSuccess {
                val intent = Intent(this@OtpVerifyActivity, MainActivity::class.java)
                startActivity(intent)
                finish()
            }

            result.onFailure { exception ->
                binding.tilOtpCode.error = exception.message
                binding.btnVerifyOtp.isEnabled = true
            }
        }
    }
}
