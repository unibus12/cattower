package com.example.smartboard;

import android.content.Intent;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.provider.MediaStore;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;

import androidx.appcompat.app.AppCompatActivity;

public class SignupActivity extends AppCompatActivity {

    EditText signup_id, signup_pwd;
    Button btnok, btncansel, btnphoto;
    ImageView imagephoto;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signup);

        btnok = (Button) findViewById(R.id.btnok);
        btncansel = (Button) findViewById(R.id.btncansel);
        btnphoto = (Button) findViewById(R.id.btnphoto);

        btnok.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), MyService.class);
                intent.putExtra("step", 1);
                intent.putExtra("mode", "회원가입,success");
                startService(intent);

                finish();
            }
        });

        btncansel.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent intent = new Intent(getApplicationContext(), MyService.class);
                intent.putExtra("step", 1);
                intent.putExtra("mode", "회원가입,cancel");
                startService(intent);

                finish();
            }
        });

        btnphoto.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), MyService.class);
                intent.putExtra("step", 1);
                intent.putExtra("mode", "얼굴등록");
                startService(intent);
            }
        });
    }
    @Override
    public void onBackPressed() {
        Intent intent = new Intent(getApplicationContext(), MyService.class);
        intent.putExtra("step", 1);
        intent.putExtra("mode","회원가입,cancel");
        startService(intent);
        super.onBackPressed();
    }

}
