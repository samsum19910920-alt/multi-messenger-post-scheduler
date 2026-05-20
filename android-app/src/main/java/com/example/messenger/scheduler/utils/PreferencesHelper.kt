package com.example.messenger.scheduler.utils

import android.content.Context
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import com.example.messenger.scheduler.data.model.User
import com.google.gson.Gson
import kotlinx.coroutines.flow.map
import javax.inject.Inject

/**
 * کلاس کمکی برای ذخیره و خواندن اطلاعات از DataStore
 */
private val Context.dataStore by preferencesDataStore(name = "app_preferences")

class PreferencesHelper @Inject constructor(private val context: Context) {

    private val gson = Gson()

    suspend fun saveToken(token: String) {
        context.dataStore.edit { preferences ->
            preferences[stringPreferencesKey("access_token")] = token
        }
    }

    fun getToken(): String? = try {
        // This should be replaced with proper Flow collection
        null
    } catch (e: Exception) {
        null
    }

    suspend fun saveUser(user: User) {
        context.dataStore.edit { preferences ->
            preferences[stringPreferencesKey("user")] = gson.toJson(user)
        }
    }

    fun getUser(): User? = try {
        // This should be replaced with proper Flow collection
        null
    } catch (e: Exception) {
        null
    }

    suspend fun clearAll() {
        context.dataStore.edit { it.clear() }
    }
}
