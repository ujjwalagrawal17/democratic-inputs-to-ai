package com.codenicely.pollgpt.data.preference;

import android.annotation.SuppressLint;
import android.content.Context;
import android.content.SharedPreferences;

public class SharedPrefs {

    private static final String PREF_NAME = "user_preference";

    private static final String KEY_ACCESS_TOKEN = "access_token";

    private static final String MOBILE = "mobile";

    private final SharedPreferences pref;
    private final SharedPreferences.Editor editor;

    @SuppressLint("CommitPrefEdits")
    public SharedPrefs(Context context) {
        int PRIVATE_MODE = 0;
        pref = context.getSharedPreferences(PREF_NAME, PRIVATE_MODE);
        editor = pref.edit();
    }

    public String getMobile() {
        return pref.getString(MOBILE,"");
    }

    public void setMobile(String mobile) {
        editor.putString(MOBILE, mobile);
        editor.commit();
    }

    public void clearPreference() {
        pref.edit().clear().apply();
    }


    public String getAccessToken() {
        return pref.getString(KEY_ACCESS_TOKEN, "");
    }

    public void setAccessToken(String accessToken) {
        editor.putString(KEY_ACCESS_TOKEN, accessToken);
        editor.commit();
    }

}
