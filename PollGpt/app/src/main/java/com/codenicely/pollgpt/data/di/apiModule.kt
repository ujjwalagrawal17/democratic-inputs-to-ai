import android.os.Build
import android.util.Log
import com.chuckerteam.chucker.api.ChuckerCollector
import com.chuckerteam.chucker.api.ChuckerInterceptor
import com.codenicely.pollgpt.BaseApplication.Companion.context
import com.codenicely.pollgpt.BuildConfig
import com.codenicely.pollgpt.data.preference.SharedPrefs
import com.codenicely.pollgpt.utils.Urls
import com.google.gson.Gson
import com.google.gson.GsonBuilder
import com.jakewharton.retrofit2.adapter.kotlin.coroutines.CoroutineCallAdapterFactory
import okhttp3.Interceptor
import okhttp3.OkHttpClient
import okhttp3.Response
import okhttp3.logging.HttpLoggingInterceptor
//import org.koin.dsl.module
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.create
import java.lang.Exception
import java.util.concurrent.TimeUnit


/**
 * Use the [apiModule] to creating Retrofit2 api service
 * for WikiEduDashboardApi
 *
 * @return retrofit.create(WikiEduDashboardApi::class.java) */
//val apiModule = module {
//
//    factory { AuthInterceptor(get()) }
//    factory { NetworkInterceptor(get()) }
//    factory { provideOkHttpClient(get(), get()) }
//    single { provideBaseRetrofit(get()) }
//    single { ResponseHandler() }
//    single { provideBaseRetrofit(get()).create(SplashApi::class.java) }
//
//}

/**
 * Use the [providerGSON] to provide GSON
 * @return GSONBuilder*/
fun providerGSON(): Gson =
    GsonBuilder()
        .setLenient()
        .serializeNulls()
        .create()

/**
 * Use the [provideInterceptor] to provide a HttpLoggingInterceptor
 * @return HttpLoggingInterceptor*/
fun provideInterceptor(): HttpLoggingInterceptor {
    val interceptor = HttpLoggingInterceptor()
    interceptor.level = HttpLoggingInterceptor.Level.BODY

    return interceptor
}

class AuthInterceptorWithNoCompanyId(sharedPrefs: SharedPrefs) : Interceptor {
    private var sharedPrefsLocal: SharedPrefs = sharedPrefs
    override fun intercept(chain: Interceptor.Chain): Response {
        var req = chain.request()
        var url = req.url

        val accessToken = sharedPrefsLocal.accessToken

//        val otpToken = sharedPrefsLocal.otpToken
        if (accessToken != "") {
            Log.d("tokenAya", accessToken)
            req = req.newBuilder()
                .header("Authorization", "Bearer $accessToken")
                .url(url).build()
        }
        val response = chain.proceed(req)
        try {
//            Timber.d("response: %s", response.peekBody(2048).string())
        } catch (e: Exception) {
            e.printStackTrace()
        }
        return response

    }

}

class AuthInterceptor(sharedPrefs: SharedPrefs) : Interceptor {

    private var sharedPrefsLocal: SharedPrefs = sharedPrefs

    override fun intercept(chain: Interceptor.Chain): Response {
        var req = chain.request()
        var url = req.url



        Log.d("urlAttacked1", url.toString());


        val accessToken = sharedPrefsLocal.accessToken

        Log.d("urlAttacked2", url.toString());


        if (accessToken != "") {
            Log.d("tokenAya", accessToken)
            req = req.newBuilder()
                .header("Authorization", "Bearer $accessToken")
                .url(url).build()
            if (!url.toString().contains("auth"))
                url = url.newBuilder().build()
                req = req.newBuilder()
                    .header("Authorization", "Bearer $accessToken")
                    .url(url).build()
        }

        val response = chain.proceed(req)

        try {

        } catch (e: Exception) {
            e.printStackTrace()
        }
        return response
    }
}


class NetworkInterceptor(sharedPrefs: SharedPrefs) : Interceptor {

    private var sharedPrefsLocal: SharedPrefs = sharedPrefs
    override fun intercept(chain: Interceptor.Chain): Response {

        val response = chain.proceed(chain.request());

        val accessToken = response.headers.get("access-token")

        if (accessToken != null) {


            sharedPrefsLocal.accessToken = accessToken

        }


        return response
    }


}


/**
 * Use the [provide Client] to provide a OkHttpClient
 * @return OkHttpClient*/
//fun provideOkHttpClient(authInterceptor: AuthInterceptor, networkInterceptor: NetworkInterceptor): OkHttpClient =
//    OkHttpClient.Builder()
//        .addInterceptor(authInterceptor)
//        .addInterceptor(provideInterceptor())
//        .addInterceptor(networkInterceptor)
//        .connectTimeout(5, TimeUnit.MINUTES)
//        .readTimeout(5, TimeUnit.MINUTES)
////        .authenticator(TokenAuthenticator())
//        .build()


fun provideOkHttpClient(
    authInterceptor: AuthInterceptor,
    networkInterceptor: NetworkInterceptor
): OkHttpClient {
    return if (BuildConfig.DEBUG) {
        OkHttpClient.Builder()
            .addInterceptor(authInterceptor)
            .addInterceptor(
                ChuckerInterceptor.Builder(context!!)
                    .collector(ChuckerCollector(context!!))
                    .maxContentLength(250000L)
                    .redactHeaders(emptySet())
                    .alwaysReadResponseBody(false)
                    .build()
            )
            .addInterceptor(provideInterceptor())
            .addInterceptor(networkInterceptor)
            .connectTimeout(5, TimeUnit.MINUTES)
            .readTimeout(5, TimeUnit.MINUTES)
//        .authenticator(TokenAuthenticator())
            .build()
    }else{
        OkHttpClient.Builder()
        .addInterceptor(authInterceptor)
        .addInterceptor(provideInterceptor())
        .addInterceptor(networkInterceptor)
        .connectTimeout(5, TimeUnit.MINUTES)
        .readTimeout(5, TimeUnit.MINUTES)
//        .authenticator(TokenAuthenticator())
        .build()
    }
}


/**
 * Use the [provideBaseRetrofit] to provide a Retrofit with WITH_BASE_URL instance
 * @return Retrofit*/
fun provideBaseRetrofit(okHttpClient: OkHttpClient): Retrofit =
    Retrofit.Builder()
        .baseUrl(Urls.BASE_URL)
        .client(okHttpClient)
        .addConverterFactory(GsonConverterFactory.create(providerGSON()))
        .addCallAdapterFactory(CoroutineCallAdapterFactory())
        .build()



