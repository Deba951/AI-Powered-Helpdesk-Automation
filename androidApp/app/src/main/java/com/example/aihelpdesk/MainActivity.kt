package com.example.aihelpdesk

import android.animation.Animator
import android.animation.AnimatorListenerAdapter
import android.os.Bundle
import android.view.View
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.android.volley.Request
import com.android.volley.RequestQueue
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley
import com.google.android.material.button.MaterialButton
import com.google.android.material.chip.Chip
import com.google.android.material.progressindicator.CircularProgressIndicator
import org.json.JSONObject

class MainActivity : AppCompatActivity() {

    private lateinit var customerNameEdit: EditText
    private lateinit var queryEdit: EditText
    private lateinit var escalateChip: Chip
    private lateinit var submitButton: MaterialButton
    private lateinit var loadingLayout: LinearLayout
    private lateinit var resultsLayout: LinearLayout
    private lateinit var categoryText: TextView
    private lateinit var priorityText: TextView
    private lateinit var confidenceText: TextView
    private lateinit var responseText: TextView
    private lateinit var salesforceStatusText: TextView

    private lateinit var requestQueue: RequestQueue

    // Replace with your API URL
    private val API_URL = "http://192.168.29.61:8000" // Your computer's IP address

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Initialize Volley request queue
        requestQueue = Volley.newRequestQueue(this)

        // Initialize views
        initializeViews()

        // Set click listener
        submitButton.setOnClickListener {
            analyzeQuery()
        }
    }

    private fun initializeViews() {
        customerNameEdit = findViewById(R.id.customerNameEdit)
        queryEdit = findViewById(R.id.queryEdit)
        escalateChip = findViewById(R.id.escalateChip)
        submitButton = findViewById(R.id.submitButton)
        loadingLayout = findViewById(R.id.loadingLayout)
        resultsLayout = findViewById(R.id.resultsLayout)
        categoryText = findViewById(R.id.categoryText)
        priorityText = findViewById(R.id.priorityText)
        confidenceText = findViewById(R.id.confidenceText)
        responseText = findViewById(R.id.responseText)
        salesforceStatusText = findViewById(R.id.salesforceStatusText)
    }

    private fun analyzeQuery() {
        val customerName = customerNameEdit.text.toString().trim()
        val query = queryEdit.text.toString().trim()
        val escalated = escalateChip.isChecked

        if (customerName.isEmpty()) {
            showError("Please enter customer name")
            customerNameEdit.requestFocus()
            return
        }

        if (query.isEmpty()) {
            showError("Please enter customer query")
            queryEdit.requestFocus()
            return
        }

        // Show loading animation
        showLoading()

        // Create JSON request
        val jsonObject = JSONObject()
        jsonObject.put("customer_name", customerName)
        jsonObject.put("query", query)
        jsonObject.put("escalated", escalated)

        val jsonObjectRequest = JsonObjectRequest(
            Request.Method.POST,
            "$API_URL/create_case",
            jsonObject,
            { response ->
                // Handle success
                handleResponse(response)
            },
            { error ->
                // Handle error
                handleError(error.message ?: "Network error occurred")
            }
        )

        // Add request to queue
        requestQueue.add(jsonObjectRequest)
    }

    private fun showLoading() {
        // Animate out results if visible
        if (resultsLayout.visibility == View.VISIBLE) {
            resultsLayout.animate()
                .alpha(0f)
                .setDuration(200)
                .setListener(object : AnimatorListenerAdapter() {
                    override fun onAnimationEnd(animation: Animator) {
                        resultsLayout.visibility = View.GONE
                        showLoadingAnimation()
                    }
                })
        } else {
            showLoadingAnimation()
        }
    }

    private fun showLoadingAnimation() {
        loadingLayout.alpha = 0f
        loadingLayout.visibility = View.VISIBLE
        submitButton.isEnabled = false

        loadingLayout.animate()
            .alpha(1f)
            .setDuration(300)
            .setListener(null)
    }

    private fun hideLoading() {
        loadingLayout.animate()
            .alpha(0f)
            .setDuration(200)
            .setListener(object : AnimatorListenerAdapter() {
                override fun onAnimationEnd(animation: Animator) {
                    loadingLayout.visibility = View.GONE
                    submitButton.isEnabled = true
                }
            })
    }

    private fun handleResponse(response: JSONObject) {
        runOnUiThread {
            hideLoading()

            try {
                // Update UI with results
                categoryText.text = response.getString("category")
                priorityText.text = getPriorityWithEmoji(response.getString("priority"))
                confidenceText.text = String.format("%.1f%%", response.getDouble("confidence") * 100)
                responseText.text = response.getString("response")

                // Salesforce status
                val caseId = response.optString("salesforce_case_id", "")
                val status = response.optString("salesforce_status", "")
                val escalated = response.getBoolean("escalated")

                if (caseId.isNotEmpty()) {
                    salesforceStatusText.text = "✅ Case created successfully!\n\n📋 Case ID: $caseId\n📊 Status: $status"
                    if (escalated) {
                        salesforceStatusText.append("\n\n🚨 Escalated to human agent")
                    }
                } else {
                    salesforceStatusText.text = "❌ Failed to create Salesforce case\n\nPlease check your backend configuration"
                }

                // Animate in results
                showResults()

            } catch (e: Exception) {
                handleError("Error parsing response: ${e.message}")
            }
        }
    }

    private fun showResults() {
        resultsLayout.alpha = 0f
        resultsLayout.visibility = View.VISIBLE

        resultsLayout.animate()
            .alpha(1f)
            .setDuration(400)
            .setListener(null)
    }

    private fun handleError(errorMessage: String) {
        runOnUiThread {
            hideLoading()

            // Show error toast with custom styling
            val toast = Toast.makeText(this, "❌ $errorMessage", Toast.LENGTH_LONG)
            val toastView = toast.view
            toastView?.setBackgroundColor(ContextCompat.getColor(this, R.color.error))
            toast.show()
        }
    }

    private fun showError(message: String) {
        val toast = Toast.makeText(this, "⚠️ $message", Toast.LENGTH_SHORT)
        val toastView = toast.view
        toastView?.setBackgroundColor(ContextCompat.getColor(this, R.color.warning))
        toast.show()
    }

    private fun getPriorityWithEmoji(priority: String): String {
        return when (priority.lowercase()) {
            "low" -> "🟢 Low Priority"
            "medium" -> "🟡 Medium Priority"
            "high" -> "🔴 High Priority"
            else -> priority
        }
    }
}
