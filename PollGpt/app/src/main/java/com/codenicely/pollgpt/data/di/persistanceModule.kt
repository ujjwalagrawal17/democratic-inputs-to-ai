package com.codenicely.gimbook.saudi.einvoice.data.di


import com.codenicely.gimbook.saudi.einvoice.data.preferences.SharedPrefs
import com.codenicely.gimbook.saudi.einvoice.utils.glide.GlideImageLoader
import org.koin.dsl.module

/**
 * Use the [persistenceModule] to creating shared preference instance
 **/
val persistenceModule = module {

    /**
     * Singleton for shared preference
     **/
    single { SharedPrefs(get()) }

    single { GlideImageLoader(get ()) }


}