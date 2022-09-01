package com.example.smartboard;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {
    Button btnsignup, btnfacelog;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Intent intent = new Intent(getApplicationContext(), MyService.class);
        startService(intent);

        btnsignup = (Button) findViewById(R.id.btnsign);
        btnfacelog = (Button) findViewById(R.id.btnfacelog);


        btnsignup.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                intent.putExtra("step", 1);
                intent.putExtra("mode","회원가입");
                startService(intent);

                Intent sign_intent = new Intent(getApplicationContext(), SignupActivity.class);
                startActivity(sign_intent);
            }
        });

        btnfacelog.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                intent.putExtra("step", 1);
                intent.putExtra("mode","로그인");
                startService(intent);

                Toast tMsg = Toast.makeText(MainActivity.this, "로그인", Toast.LENGTH_SHORT);
                tMsg.show();
                tMsg = Toast.makeText(MainActivity.this, "자리에 앉아 정면을 보세요", Toast.LENGTH_SHORT);
                tMsg.show();
            }
        });
    }

    @Override
    protected void onNewIntent(Intent intent) {
        processIntent(intent);
        super.onNewIntent(intent);
    }


    private void processIntent(Intent intent){
        String log_data = intent.getStringExtra("data");
        Log.d("TAG","login data 확인"+log_data);

        String[] array = log_data.split(",");

        if(array[1]==null){
            Toast tMsg = Toast.makeText(MainActivity.this, " ", Toast.LENGTH_SHORT);
            tMsg.show();
        }
        else if(array[1].equals("success")){
            intent.putExtra("step", 1);
            intent.putExtra("mode","메뉴");
            startService(intent);

            Toast tMsg = Toast.makeText(MainActivity.this, "로그인 성공", Toast.LENGTH_SHORT);
            tMsg.show();

            Intent menu_intent = new Intent(getApplicationContext(), MenuActivity.class);
            startActivity(menu_intent);
        }else{
            Toast tMsg = Toast.makeText(MainActivity.this, "로그인 실패\n다시 시도해 주세요", Toast.LENGTH_SHORT);
            tMsg.show();
        }

    }
}