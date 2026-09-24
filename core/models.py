from django.db import models


class Visit(models.Model):
    """
    Modelo de prueba para demostrar persistencia y operaciones ORM
    conectadas a MariaDB.
    """
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="Dirección IP")
    user_agent = models.CharField(max_length=255, blank=True, verbose_name="User Agent")

    class Meta:
        verbose_name = "Visita"
        verbose_name_plural = "Visitas"
        ordering = ['-timestamp']

    def __str__(self):
        return f"Visita #{self.id} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
