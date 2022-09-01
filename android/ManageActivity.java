package com.example.smartboard;


import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.os.Message;
import android.util.Log;
import android.os.Handler;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.SeekBar;
import android.widget.TextView;


import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;


public class ManageActivity extends Activity {
    TextView last_day, korState, engState;
    TextView korWord1, korWord2, korWord3, korWord4;
    TextView korYN1, korYN2, korYN3, korYN4;
    TextView engWord1, engWord2, engWord3, engWord4;
    TextView engYN1, engYN2, engYN3, engYN4;

    SeekBar seekBar;
    String TAG = "mytag";

    @Override
    public void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_manage);

        last_day = (TextView) findViewById(R.id.last_day);
        seekBar = (SeekBar) findViewById(R.id.corr_goal);

        korState = (TextView) findViewById(R.id.korState);
        engState = (TextView) findViewById(R.id.engState);

        korWord1 = (TextView) findViewById(R.id.korWord1);
        korWord2 = (TextView) findViewById(R.id.korWord2);
        korWord3 = (TextView) findViewById(R.id.korWord3);
        korWord4 = (TextView) findViewById(R.id.korWord4);

        korYN1 = (TextView) findViewById(R.id.korYN1);
        korYN2 = (TextView) findViewById(R.id.korYN2);
        korYN3 = (TextView) findViewById(R.id.korYN3);
        korYN4 = (TextView) findViewById(R.id.korYN4);

        engWord1 = (TextView) findViewById(R.id.engWord1);
        engWord2 = (TextView) findViewById(R.id.engWord2);
        engWord3 = (TextView) findViewById(R.id.engWord3);
        engWord4 = (TextView) findViewById(R.id.engWord4);

        engYN1 = (TextView) findViewById(R.id.engYN1);
        engYN2 = (TextView) findViewById(R.id.engYN2);
        engYN3 = (TextView) findViewById(R.id.engYN3);
        engYN4 = (TextView) findViewById(R.id.engYN4);

        // OnSeekBarChange 리스너 - Seekbar 값 변경시 이벤트처리 Listener
        seekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                // onProgressChange - Seekbar 값 변경될때마다 호출
            }
            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
                // onStartTeackingTouch - SeekBar 값 변경위해 첫 눌림에 호출
            }
            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                // onStopTrackingTouch - SeekBar 값 변경 끝나고 드래그 떼면 호출
                Log.d(TAG, String.format("onStopTrackingTouch 값 변경 종료: progress [%d]", seekBar.getProgress()));
                Intent intent = new Intent(getApplicationContext(), MyService.class);
                intent.putExtra("step", 1);
                intent.putExtra("mode","진도,"+seekBar.getProgress());
                startService(intent);
            }
        });
    }

    @Override
    // 서비스쪽에서 던져준 데이터를 받기위한 메서드이다. processCommand는 출력하기위한 메소드
    // 처음이면 oncreate에서 확인 하고 그렇지 않으면(처음이 아니라면) oncreate에서 호출되지 않고
    // onNewIntent() 를 호출 하게 된다. 서비스 -> 액티비티에서 확인하는경우.
    protected void onNewIntent(Intent intent) {
        processIntent(intent);
        super.onNewIntent(intent);
    }


    private void processIntent(Intent intent){
        int step1 = intent.getIntExtra("step",0);
        Log.d("TAG","recv step 확인");
        if(step1==3){
            Log.d("TAG","recv data 받음");
            String data = intent.getStringExtra("data");
            Log.d("TAG","data "+ data);

            String[] array = data.split(",");
            if (array[0].equals("진도")){
                last_day.setText("마지막 학습일자: "+array[1]);
                seekBar.setProgress(Integer.parseInt(array[2]));
                korState.setText(array[3]);
                if(array[3].equals("단계 1")) { // 변경
                    korWord1.setText("사과");
                    korWord2.setText("하늘");
                    korWord3.setText("안녕");
                    korWord4.setText("기린");
                } else if(array[3].equals("단계 2")){
                    korWord1.setText("비행기");
                    korWord2.setText("바나나");
                    korWord3.setText("장난감");
                    korWord4.setText("피아노");
                } else if(array[3].equals("단계 3")){
                    korWord1.setText("선생님");
                    korWord2.setText("우리나라");
                    korWord3.setText("대한민국");
                    korWord4.setText("초등학교");
                }
                korYN1.setText(array[4]);
                korYN2.setText(array[5]);
                korYN3.setText(array[6]);
                korYN4.setText(array[7]);
                engState.setText(array[8]);
                if(array[8].equals("단계 1")) { // 변경
                    engWord1.setText("sky");
                    engWord2.setText("box");
                    engWord3.setText("lam");
                    engWord4.setText("mom");
                } else if(array[8].equals("단계 2")){
                    engWord1.setText("good");
                    engWord2.setText("apple");
                    engWord3.setText("hello");
                    engWord4.setText("korea");
                } else if(array[8].equals("단계 3")){
                    engWord1.setText("pencil");
                    engWord2.setText("window");
                    engWord3.setText("airplane");
                    engWord4.setText("building");
                }
                engYN1.setText(array[9]);
                engYN2.setText(array[10]);
                engYN3.setText(array[11]);
                engYN4.setText(array[12]);
            }
        }
    }
}
