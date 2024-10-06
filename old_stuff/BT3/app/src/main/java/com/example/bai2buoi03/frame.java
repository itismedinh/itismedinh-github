package com.example.bai2buoi03;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

public class frame extends Fragment {

    private TextView resultTextView;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.framelayout, container, false);
        resultTextView = view.findViewById(R.id.textView1);
        return view;
    }

    public void setResult(String fullName) {
        if (resultTextView != null) {
            resultTextView.setText(fullName);
        }
    }
}