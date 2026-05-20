package com.example.messenger.scheduler.ui.auth

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.example.messenger.scheduler.databinding.ActivityLoginBinding
import com.example.messenger.scheduler.data.repository.AppRepository
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.launch
import javax.inject.Inject

/**
 * صفحه ورود - دریافت شماره تلفن و ارسال OTP
 */
@AndroidEntryPoint
class LoginActivity : AppCompatActivity() {

    private lateinit var binding: ActivityLoginBinding

    @Inject
    lateinit var repository: AppRepository

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityLoginBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupListeners()
    }

    private fun setupListeners() {
        binding.btnSendOtp.setOnClickListener {
            val phoneNumber = binding.etPhoneNumber.text.toString()
            if (phoneNumber.isNotEmpty()) {
                sendOtp(phoneNumber)
            } else {
                binding.tilPhoneNumber.error = "شماره تلفن الزامی است"
            }
        }
    }

    private fun sendOtp(phoneNumber: String) {
        lifecycleScope.launch {
            binding.btnSendOtp.isEnabled = false
            binding.btnSendOtp.text = "درحال ارسال..."

            val result = repository.sendOtp(phoneNumber)

            result.onSuccess {
                val intent = Intent(this@LoginActivity, OtpVerifyActivity::class.java).apply {
                    putExtra("phone_number", phoneNumber)
                }
                startActivity(intent)
                finish()
            }

            result.onFailure { exception ->
                binding.tilPhoneNumber.error = exception.message
                binding.btnSendOtp.isEnabled = true
                binding.btnSendOtp.text = "ارسال OTP"
            }
        }
    }
}
