package com.example.smartboard;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.SeekBar;
import android.widget.TextView;

public class ProgressActivity extends Activity {
    Button button_detail;
    TextView progress_han, progress_eng;
    ProgressBar han_progress, eng_progress;

    @Override
    public void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_progress);

        button_detail =(Button) findViewById(R.id.progress_detail);
        progress_han =(TextView) findViewById(R.id.progress_han);
        progress_eng =(TextView) findViewById(R.id.progress_eng);

        han_progress =(ProgressBar) findViewById(R.id.han_progress);
        eng_progress =(ProgressBar) findViewById(R.id.eng_progress);

        button_detail.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), MyService.class);
                intent.putExtra("step", 1);
                intent.putExtra("mode","진도");
                startService(intent);

                Intent manage_intent = new Intent(getApplicationContext(), ManageActivity.class);
                startActivity(manage_intent);
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
        int n;
        char v;
        int i;
        String Intdata1 = "";
        String Intdata2 = "";
        int k = 0;
        int step1 = intent.getIntExtra("step",0);
        Log.d("TAG","recv step 확인");
        if(step1==3){
            Log.d("TAG","recv data 받음");
            String data = intent.getStringExtra("data");
            Log.d("TAG","data "+ data);

            String[] array = data.split(",");
            if (array[0].equals("정보")){
                Log.d("TAG","data1 ");
                Intdata1 = array[1];
                Log.d("TAG","숫자1 "+ Intdata1);
                Intdata2 = array[2];
                Log.d("TAG","숫자2 "+ Intdata2);
            }

            Log.d("data", String.valueOf(data.length()));
            progress_han.setText(Intdata1+"%");
            progress_eng.setText(Intdata2+"%");
            han_progress.setProgress(Integer.parseInt(Intdata1));
            eng_progress.setProgress(Integer.parseInt(Intdata2));
        }
    }

}
