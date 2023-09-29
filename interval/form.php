<?php
// Database connection parameters
$host = "107.180.27.240";
$username = "meeroh";
$password = "?i*c6IV28Q%Y";
$database = "interval";

// Create a connection to the MySQL database
$mysqli = new mysqli($host, $username, $password, $database);

// Check connection
if ($mysqli->connect_error) {
    die("Connection failed: " . $mysqli->connect_error);
}

// Get data from the form
$name = $_POST['name'];
$email = $_POST['email'];

// Insert data into the database
$query = "INSERT INTO your_table (name, email) VALUES ('$name', '$email')";

if ($mysqli->query($query) === TRUE) {
    echo "Data inserted successfully.";
} else {
    echo "Error: " . $query . "<br>" . $mysqli->error;
}

// Close the database connection
$mysqli->close();
?>
