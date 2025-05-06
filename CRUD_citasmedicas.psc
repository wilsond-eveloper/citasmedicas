Proceso CRUD_citasmedicas
		// Estructura para almacenar datos completos de pacientes (5 campos)
		Dimension id[100], nombres[100], telefonos[100], emails[100], estados[100]
		Definir aElegir, cantidad, i, posicion Como Entero
		Definir nombre, telefono, email, confirmacion Como Cadena
		
		// Iniciar el contador de pacientes
		cantidad <- 0
	
		Repetir
			Escribir "----- MEN� PRINCIPAL -----"
			Escribir "1. Crear paciente"
			Escribir "2. Leer pacientes"
			Escribir "3. Actualizar pacientes"
			Escribir "4. Eliminar pacientes"
			Escribir "5. Salir"
			Escribir "Seleccione una opci�n: "
			Leer aElegir
			
			Segun aElegir Hacer
				
				Caso 1: // Crear
					Si cantidad < 100 Entonces
						Escribir "=== REGISTRO DE NUEVO PACIENTE ==="
						Escribir "Ingrese nombre del paciente:"
						Leer nombre
						Escribir "Ingrese tel�fono del paciente:"
						Leer telefono
						Escribir "Ingrese email del paciente:"
						Leer email
						
						// Incrementamos cantidad antes para usar �ndices desde 1
						cantidad <- cantidad + 1
						
						// Guardar datos del paciente (�ndices desde 1)
						id[cantidad] <- cantidad     // ID = posici�n
						nombres[cantidad] <- nombre
						telefonos[cantidad] <- telefono
						emails[cantidad] <- email
						estados[cantidad] <- "Activo"
						
						Escribir "Paciente registrado con exito. "
					Sino
						Escribir "Error: Base de datos llena. No se pueden registrar m�s pacientes."
					FinSi
					
				Caso 2: // Leer
					Si cantidad = 0 Entonces
						Escribir "No hay pacientes registrados en el sistema."
					Sino
						Escribir "=== LISTADO DE PACIENTES ==="
						Escribir "ID | NOMBRE | TEL�FONO | EMAIL | ESTADO"
						Para i <- 1 Hasta cantidad Con Paso 1 Hacer
							Escribir id[i], " | ", nombres[i], " | ", telefonos[i], " | ", emails[i], " | ", estados[i]
						FinPara
						
						Escribir "�Desea ver detalles de alg�n paciente? (S/N)"
						Leer confirmacion
						Si confirmacion = "S" O confirmacion = "s" Entonces
							Escribir "Ingrese ID del paciente:"
							Leer posicion
							
							encontrado <- Falso
							Para i <- 1 Hasta cantidad Con Paso 1 Hacer
								Si id[i] = posicion Entonces
									Escribir "=== DETALLES DEL PACIENTE ==="
									Escribir "ID: ", id[i]
									Escribir "Nombre: ", nombres[i]
									Escribir "Tel�fono: ", telefonos[i]
									Escribir "Email: ", emails[i]
									Escribir "Estado: ", estados[i]
									encontrado <- Verdadero
								FinSi
							FinPara
							
							Si No encontrado Entonces
								Escribir "No se encontr� un paciente con el ID especificado."
							FinSi
						FinSi
					FinSi
					
				Caso 3: // Actualizar
					Si cantidad = 0 Entonces
						Escribir "No hay pacientes registrados para actualizar."
					Sino
						Escribir "=== ACTUALIZAR PACIENTE ==="
						Escribir "Ingrese ID del paciente a actualizar:"
						Leer posicion
						
						encontrado <- Falso
						Para i <- 1 Hasta cantidad Con Paso 1 Hacer
							Si id[i] = posicion Entonces
								Escribir "Paciente encontrado:"
								Escribir "Nombre actual: ", nombres[i]
								Escribir "Tel�fono actual: ", telefonos[i]
								Escribir "Email actual: ", emails[i]
								
								Escribir "Ingrese nuevo nombre (o Enter para mantener el actual):"
								Leer nombre
								Si nombre <> "" Entonces
									nombres[i] <- nombre
								FinSi
								
								Escribir "Ingrese nuevo tel�fono (o Enter para mantener el actual):"
								Leer telefono
								Si telefono <> "" Entonces
									telefonos[i] <- telefono
								FinSi
								
								Escribir "Ingrese nuevo email (o Enter para mantener el actual):"
								Leer email
								Si email <> "" Entonces
									emails[i] <- email
								FinSi
								
								Escribir "�Paciente actualizado correctamente!"
								encontrado <- Verdadero
							FinSi
						FinPara
						
						Si No encontrado Entonces
							Escribir "No se encontr� un paciente con el ID especificado."
						FinSi
					FinSi
					
				Caso 4: // Eliminar
					Si cantidad = 0 Entonces
						Escribir "No hay pacientes registrados para eliminar."
					Sino
						Escribir "=== ELIMINAR PACIENTE ==="
						Escribir "Ingrese ID del paciente a eliminar:"
						Leer posicion
						
						encontrado <- Falso
						Para i <- 1 Hasta cantidad Con Paso 1 Hacer
							Si id[i] = posicion Entonces
								Escribir "Paciente encontrado:"
								Escribir "Nombre: ", nombres[i]
								Escribir "Tel�fono: ", telefonos[i]
								Escribir "Email: ", emails[i]
								
								Escribir "�Est� seguro que desea eliminar este paciente? (S/N)"
								Leer confirmacion
								
								Si confirmacion = "S" O confirmacion = "s" Entonces
									// Opci�n 1: Eliminaci�n l�gica (marcar como inactivo)
									estados[i] <- "Inactivo"
									Escribir "Paciente marcado como inactivo correctamente."
									
									// Opci�n 2: Eliminaci�n f�sica (reordenar arreglo)
									Para j <- i Hasta cantidad - 1 Con Paso 1 Hacer
										id[j] <- id[j+1]
										nombres[j] <- nombres[j+1]
										telefonos[j] <- telefonos[j+1]
										emails[j] <- emails[j+1]
										estados[j] <- estados[j+1]
									FinPara
									cantidad <- cantidad - 1
									Escribir "Paciente eliminado correctamente."
									
								Sino
									Escribir "Operaci�n cancelada."
								FinSi
								
								encontrado <- Verdadero
							FinSi
						FinPara
						
						Si No encontrado Entonces
							Escribir "No se encontr� un paciente con el ID especificado."
						FinSi
					FinSi
					
				Caso 5: // Salir
					Escribir "�Est� seguro que desea salir del sistema? (S/N)"
					Leer confirmacion
					Si confirmacion <> "S" Y confirmacion <> "s" Entonces
						aElegir <- 0  // Volver al men� si no confirma
					Sino
						Escribir "Gracias por utilizar el sistema de citas m�dicas."
					FinSi
					
				De Otro Modo:
					Escribir "Opci�n inv�lida. Intente nuevamente."
					
			FinSegun
			
			Si aElegir <> 5 Entonces
				Leer confirmacion  // Pausa para que el usuario pueda leer los resultados
			FinSi
			
		Hasta Que aElegir = 5 Y (confirmacion = "S" O confirmacion = "s")
FinProceso