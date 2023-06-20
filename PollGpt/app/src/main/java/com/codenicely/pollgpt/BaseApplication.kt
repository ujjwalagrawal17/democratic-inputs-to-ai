package com.codenicely.pollgpt

import android.app.Application
//import apiModule
//import org.koin.android.ext.koin.androidContext
//import org.koin.core.context.startKoin

class BaseApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        context = this
//        startKoin {
//            androidContext(this@BaseApplication)
////            modules(listOf(apiModule, persistenceModule, repositoryModule, viewModelModule))
//
//        }


    }

    companion object {
        var context: BaseApplication? = null

    }

}




