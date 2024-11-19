<?php
// Contact form handler

// Email configuration
$config = array(
    'smtp_host' => 'mail.christopherdanielbradford.com',
    'smtp_port' => 465,
    'smtp_username' => 'contact@christopherdanielbradford.com',
    'recipient_email' => 'contact@christopherdanielbradford.com',
    'use_smtp_auth' => true,
    'use_smtp_ssl' => true
);

// Validate form data
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = filter_var($_POST["name"] ?? '', FILTER_SANITIZE_STRING);
    $email = filter_var($_POST["email"] ?? '', FILTER_SANITIZE_EMAIL);
    $message = filter_var($_POST["message"] ?? '', FILTER_SANITIZE_STRING);
    
    // Basic validation
    if (empty($name) || empty($email) || empty($message)) {
        http_response_code(400);
        echo json_encode(["error" => "All fields are required"]);
        exit;
    }
    
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        http_response_code(400);
        echo json_encode(["error" => "Invalid email format"]);
        exit;
    }
    
    // Prepare email
    $to = $config['recipient_email'];
    $subject = "Contact Form Submission from " . $name;
    $email_content = "Name: " . $name . "\n";
    $email_content .= "Email: " . $email . "\n\n";
    $email_content .= "Message:\n" . $message;
    
    // Email headers
    $headers = array(
        'From: ' . $email,
        'Reply-To: ' . $email,
        'X-Mailer: PHP/' . phpversion(),
        'Content-Type: text/plain; charset=UTF-8'
    );
    
    // Send email
    if (mail($to, $subject, $email_content, implode("\r\n", $headers))) {
        http_response_code(200);
        echo json_encode(["message" => "Thank you for your message. I will get back to you soon!"]);
    } else {
        http_response_code(500);
        echo json_encode(["error" => "Failed to send message. Please try again later."]);
    }
} else {
    http_response_code(405);
    echo json_encode(["error" => "Method not allowed"]);
}
?>
