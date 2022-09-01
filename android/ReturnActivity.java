package com.example.smartboard;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class ReturnActivity  extends Activity {
    TextView bluereturn, ModeStr;
    Button btnend;
    int i = 0;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_return);
        ModeStr = (TextView) findViewById(R.id.ModeStr);
        bluereturn = (TextView) findViewById(R.id.bluereturn);
        btnend = (Button) findViewById(R.id.btnend);

        btnend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), MyService.class);
                intent.putExtra("step", 1);
                intent.putExtra("mode","메뉴");
                startService(intent);
                finish();
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
        int step = intent.getIntExtra("step",0);
        Log.d("TAG","recv step 확인");
        if(step==3){
            Log.d("TAG","recv data 받음");
            String data = intent.getStringExtra("data");
            Log.d("TAG","data "+data);
            String[] array = data.split(",");
            if(array.length==4) {
                if (array[1].equals("한글") && array[2].equals("1")) {
                    ModeStr.setText("자음, 모음 학습");
                } else if (array[1].equals("한글") && array[2].equals("2")) {
                    ModeStr.setText("한글 단어, 문장 학습");
                } else if (array[1].equals("한글") && array[2].equals("3")) {
                    ModeStr.setText("한글 게임");
                } else if (array[1].equals("영어") && array[2].equals("1")) {
                    ModeStr.setText("알파벳 학습");
                } else if (array[1].equals("영어") && array[2].equals("2")) {
                    ModeStr.setText("영어 단어, 문장 학습");
                } else if (array[1].equals("영어") && array[2].equals("3")) {
                    ModeStr.setText("영어 게임");
                } else if (array[1].equals("한글")) {
                    ModeStr.setText("한글 : 모드 선택되지 않음");
                } else if (array[1].equals("영어")) {
                    ModeStr.setText("영어 : 모드 선택되지 않음");
                } else if (array[1].equals("한영")) {
                    ModeStr.setText("언어 선택대기중");
                } else {
                    ModeStr.setText("error");
                }
                if (array[3] != "") {
                    bluereturn.setText(array[3]);
                } else {
                    bluereturn.setText("입력 대기중");
                }
            }
            else if(array.length==3) {
                if (array[1].equals("한글") && array[2].equals("1")) {
                    ModeStr.setText("자음, 모음 학습");
                } else if (array[1].equals("한글") && array[2].equals("2")) {
                    ModeStr.setText("한글 단어, 문장 학습");
                } else if (array[1].equals("한글") && array[2].equals("3")) {
                    ModeStr.setText("한글 게임");
                } else if (array[1].equals("영어") && array[2].equals("1")) {
                    ModeStr.setText("알파벳 학습");
                } else if (array[1].equals("영어") && array[2].equals("2")) {
                    ModeStr.setText("영어 단어, 문장 학습");
                } else if (array[1].equals("영어") && array[2].equals("3")) {
                    ModeStr.setText("영어 게임");
                } else if (array[1].equals("한글")) {
                    ModeStr.setText("한글 : 모드 선택되지 않음");
                } else if (array[1].equals("영어")) {
                    ModeStr.setText("영어 : 모드 선택되지 않음");
                } else if (array[1].equals("한영")) {
                    ModeStr.setText("언어 선택대기중");
                } else {
                    ModeStr.setText("error");
                }
                bluereturn.setText("입력 대기중");
            }
            else if(array.length==2) {
                if (array[1].equals("한영")) {
                    ModeStr.setText("언어 선택대기중");
                    bluereturn.setText("");
                } else if (array[1].equals("한글")) {
                    ModeStr.setText("한글");
                    bluereturn.setText("모드 선택되지 않음");
                } else if (array[1].equals("영어")) {
                    ModeStr.setText("영어");
                    bluereturn.setText("모드 선택되지 않음");
                }
            }
        }
    }

    @Override
    public void onBackPressed() {
        Intent intent = new Intent(getApplicationContext(), MyService.class);
        intent.putExtra("step", 1);
        intent.putExtra("mode","메뉴");
        startService(intent);
        finish();
        super.onBackPressed();
    }
}