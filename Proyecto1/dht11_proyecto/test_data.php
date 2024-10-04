<?php
$hostname = "localhost"; 
$username = "root"; 
$password = ""; 
$database = "arqbased"; 

// Conexión a la base de datos
$conn = mysqli_connect($hostname, $username, $password, $database);

if (!$conn) { 
    die("Connection failed: " . mysqli_connect_error()); 
} 

echo "Database connection is OK<br>"; 

// Generar valores aleatorios de temperatura y humedad entre 0 y 100
$t = rand(15, 35);  // Temperatura 
$h = rand(30, 70);  // Humedad 

// Insertar datos en la base de datos
$sql = "INSERT INTO clima (temperatura, humedad, id_administrador) VALUES (".$t.", ".$h.", 1)"; 

if (mysqli_query($conn, $sql)) { 
    echo "New record created successfully"; 
} else { 
    echo "Error: " . $sql . "<br>" . mysqli_error($conn); 
}

// Cerrar la conexión
mysqli_close($conn);
?>