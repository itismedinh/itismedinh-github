package com.example.bai2buoi03;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.FragmentManager;


public class MainActivity extends AppCompatActivity {

    private EditText editTextFirstName;
    private EditText editTextLastName;
    private Button buttonOk;
    private frame resultFragment;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        editTextFirstName = findViewById(R.id.data1);
        editTextLastName = findViewById(R.id.data2);

        FragmentManager fragmentManager = getSupportFragmentManager();
        resultFragment = (frame) fragmentManager.findFragmentById(R.id.fragmentContainer);

        buttonOk = findViewById(R.id.OKBT);
        buttonOk.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String firstName = editTextFirstName.getText().toString();
                String lastName = editTextLastName.getText().toString();
                String fullName = firstName + " " + lastName;

                if (resultFragment != null) {
                    resultFragment.setResult(fullName);
                }
            }
        });
    }
}