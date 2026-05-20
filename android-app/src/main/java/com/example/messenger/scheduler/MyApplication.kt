package com.example.messenger.scheduler

import android.app.Application
import dagger.hilt.android.HiltAndroidApp

/**
 * نقطه ورودی اپلیکیشن - Hilt Dependency Injection را راه‌اندازی می‌کند
 */
@HiltAndroidApp
class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()
    }
}
