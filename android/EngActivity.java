package com.example.smartboard;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

public class EngActivity extends Activity {
    Button btn_eng_mode1, btn_eng_mode2, btn_eng_mode3;

    @Override
    public void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_eng);

        btn_eng_mode1 = (Button) findViewById(R.id.btn_eng_mode1);
        btn_eng_mode2 = (Button) findViewById(R.id.btn_eng_mode2);
        btn_eng_mode3 = (Button) findViewById(R.id.btn_eng_mode3);

        btn_eng_mode1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Toast tMsg = Toast.makeText(EngActivity.this, "영어 자음 모음 학습 시작", Toast.LENGTH_SHORT);
                tMsg.show();

                Intent intent = new Intent(getApplicationContext(), MyService.class);
                intent.putExtra("step", 1);
                intent.putExtra("mode","영어,1");
                startService(intent);
            }
        });

        btn_eng_mode2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Toast tMsg = Toast.makeText(EngActivity.this, "영어 단어 문장 학습 시작", Toast.LENGTH_SHORT);
                tMsg.show();
                Intent intent = new Intent(getApplicationContext(), MyService.class);
                intent.putExtra("step", 1);
                intent.putExtra("mode","영어,2");
                startService(intent);
            }
        });

        btn_eng_mode3.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Toast tMsg = Toast.makeText(EngActivity.this, "영어 게임 시작", Toast.LENGTH_SHORT);
                tMsg.show();

                Intent intent = new Intent(getApplicationContext(), MyService.class);
                intent.putExtra("step", 1);
                intent.putExtra("mode","영어,3");
                startService(intent);
            }
        });
    }
}
