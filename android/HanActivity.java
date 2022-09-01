package com.example.smartboard;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

public class HanActivity extends Activity {
    Button btn_kor_mode1, btn_kor_mode2, btn_kor_mode3;

    @Override
    public void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_han);

        btn_kor_mode1 = (Button) findViewById(R.id.btn_kor_mode1);
        btn_kor_mode2 = (Button) findViewById(R.id.btn_kor_mode2);
        btn_kor_mode3 = (Button) findViewById(R.id.btn_kor_mode3);

        btn_kor_mode1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Toast tMsg = Toast.makeText(HanActivity.this, "한글 자음 모음 학습 시작", Toast.LENGTH_SHORT);
                tMsg.show();

                Log.d("TAG", "한글 모드1 눌림");
                Intent intent = new Intent(getApplicationContext(), MyService.class);
                intent.putExtra("step", 1);
                intent.putExtra("mode","한글,1");
                startService(intent);
            }
        });

        btn_kor_mode2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Toast tMsg = Toast.makeText(HanActivity.this, "한글 단어 문장 학습 시작", Toast.LENGTH_SHORT);
                tMsg.show();

                Log.d("TAG", "한글 모드2 눌림");
                Intent intent = new Intent(getApplicationContext(), MyService.class);
                intent.putExtra("step", 1);
                intent.putExtra("mode","한글,2");
                startService(intent);
            }
        });

        btn_kor_mode3.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Toast tMsg = Toast.makeText(HanActivity.this, "한글 게임 시작", Toast.LENGTH_SHORT);
                tMsg.show();

                Log.d("TAG", "한글 모드1 눌림");
                Intent intent = new Intent(getApplicationContext(), MyService.class);
                intent.putExtra("step", 1);
                intent.putExtra("mode","한글,3");
                startService(intent);
            }
        });
    }
}
