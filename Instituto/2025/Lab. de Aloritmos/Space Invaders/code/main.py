import pygame, sys
import json
import os
from player import Player
import obstacle
from alien import Alien, Extra
from random import choice, randint
from laser import Laser

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)

def get_resource_path(filename):
    return os.path.join(PARENT_DIR, filename)

ancho_pantalla = 800
alto_pantalla = 700

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS_OSCURO = (30, 30, 30)
ROJO = (241, 79, 80)
VERDE = (80, 241, 80)

niveles_volumen = {
    "musica": 0.2,
    "efectos": 0.5
}

def cargar_puntuacion_maxima():
    archivo_puntuacion = get_resource_path('highscore.json')
    if os.path.exists(archivo_puntuacion):
        try:
            with open(archivo_puntuacion, 'r') as archivo:
                datos = json.load(archivo)
                return datos.get('puntuacion_maxima', 0)
        except:
            return 0
    return 0

def guardar_puntuacion_maxima(puntuacion):
    archivo_puntuacion = get_resource_path('highscore.json')
    try:
        with open(archivo_puntuacion, 'w') as archivo:
            json.dump({'puntuacion_maxima': puntuacion}, archivo)
    except Exception as e:
        print(f"Error al guardar puntuación: {e}")

class Boton:
    def __init__(self, texto, ancho, alto, pos, fuente):
        self.texto = texto
        self.ancho = ancho
        self.alto = alto
        self.pos = pos
        self.fuente = fuente
        self.rect = pygame.Rect(pos[0], pos[1], ancho, alto)
        self.click = False
        
    def dibujar(self, pantalla):
        pos_raton = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(pos_raton)
        
        color_boton = (200, 200, 200) if self.hover else (100, 100, 100)
        color_texto = (0, 0, 0) if self.hover else (255, 255, 255)
        
        pygame.draw.rect(pantalla, color_boton, self.rect)
        pygame.draw.rect(pantalla, (255, 255, 255), self.rect, 2)
        
        superficie_texto = self.fuente.render(self.texto, True, color_texto)
        ancho_texto = superficie_texto.get_width()
        alto_texto = superficie_texto.get_height()
        x_texto = self.pos[0] + (self.ancho - ancho_texto) // 2
        y_texto = self.pos[1] + (self.alto - alto_texto) // 2
        pantalla.blit(superficie_texto, (x_texto, y_texto))
        
        return self.hover

def mostrar_menu():
    pantalla.fill(GRIS_OSCURO)
    pos_raton = pygame.mouse.get_pos()
    
    try:
        logo = pygame.image.load(r'Personal\Space Invaders (Juego - 2025)\graphics\logo.png').convert_alpha()
        ancho_logo = min(400, ancho_pantalla * 0.7)
        alto_logo = ancho_logo * (logo.get_height() / logo.get_width())
        logo = pygame.transform.scale(logo, (int(ancho_logo), int(alto_logo)))
        x_logo = (ancho_pantalla - logo.get_width()) // 2
        y_logo = 50
        pantalla.blit(logo, (x_logo, y_logo))
        inicio_y = y_logo + logo.get_height() + 50
    except:
        print("No se pudo cargar el logo.png. Verifica que exista en la carpeta graphics.")
        inicio_y = 100
    
    ancho_boton = 200
    alto_boton = 50
    espacio_boton = 20
    
    botones = []
    opciones_menu = ["Jugar", "Multijugador", "Opciones", "Salir"]
    
    for i, opcion in enumerate(opciones_menu):
        x_boton = (ancho_pantalla - ancho_boton) // 2
        y_boton = inicio_y + i * (alto_boton + espacio_boton)
        
        boton = Boton(opcion, ancho_boton, alto_boton, (x_boton, y_boton), fuente)
        hover = boton.dibujar(pantalla)
        botones.append((boton, opcion))
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            for boton, opcion in botones:
                if boton.rect.collidepoint(pos_raton):
                    print(f"Seleccionaste: {opcion}")
                    if opcion == "Salir":
                        pygame.quit()
                        sys.exit()
                    elif opcion == "Jugar":
                        iniciar_cuenta_atras()
                        return {"accion": "jugar", "modo": "individual"}
                    elif opcion == "Multijugador":
                        iniciar_cuenta_atras()
                        return {"accion": "jugar", "modo": "multi"}
                    elif opcion == "Opciones":
                        return {"accion": "opciones"}
                    
    return {"accion": "menu"}

def mostrar_opciones():
    pantalla.fill(GRIS_OSCURO)
   
    titulo = fuente_grande.render("OPCIONES", True, BLANCO)
    rect_titulo = titulo.get_rect(center=(ancho_pantalla//2, 100))
    pantalla.blit(titulo, rect_titulo)
   
    fuente_opciones = pygame.font.Font('font/Pixeled.ttf', 14)
   
    texto_musica = fuente_opciones.render("Música: " + str(int(niveles_volumen["musica"]*100)) + "%", True, BLANCO)
    rect_texto_musica = texto_musica.get_rect(center=(ancho_pantalla//2, 200))
    pantalla.blit(texto_musica, rect_texto_musica)
   
    texto_efectos = fuente_opciones.render("Efectos: " + str(int(niveles_volumen["efectos"]*100)) + "%", True, BLANCO)
    rect_texto_efectos = texto_efectos.get_rect(center=(ancho_pantalla//2, 300))
    pantalla.blit(texto_efectos, rect_texto_efectos)
   
    boton_musica_menos = Boton("-", 50, 50, (ancho_pantalla//2 - 150, 180), fuente)
    boton_musica_menos.dibujar(pantalla)
   
    boton_musica_mas = Boton("+", 50, 50, (ancho_pantalla//2 + 100, 180), fuente)
    boton_musica_mas.dibujar(pantalla)
   
    boton_efectos_menos = Boton("-", 50, 50, (ancho_pantalla//2 - 150, 280), fuente)
    boton_efectos_menos.dibujar(pantalla)
   
    boton_efectos_mas = Boton("+", 50, 50, (ancho_pantalla//2 + 100, 280), fuente)
    boton_efectos_mas.dibujar(pantalla)
   
    boton_volver = Boton("Volver", 200, 50, ((ancho_pantalla - 200)//2, 400), fuente)
    boton_volver.dibujar(pantalla)
   
    pos_raton = pygame.mouse.get_pos()
   
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_volver.rect.collidepoint(pos_raton):
                return {"accion": "menu"}
           
            if boton_musica_menos.rect.collidepoint(pos_raton):
                niveles_volumen["musica"] = max(0.0, round(niveles_volumen["musica"] - 0.1, 1))
                actualizar_volumenes()
            elif boton_musica_mas.rect.collidepoint(pos_raton):
                niveles_volumen["musica"] = min(1.0, round(niveles_volumen["musica"] + 0.1, 1))
                actualizar_volumenes()
               
            if boton_efectos_menos.rect.collidepoint(pos_raton):
                niveles_volumen["efectos"] = max(0.0, round(niveles_volumen["efectos"] - 0.1, 1))
                actualizar_volumenes()
            elif boton_efectos_mas.rect.collidepoint(pos_raton):
                niveles_volumen["efectos"] = min(1.0, round(niveles_volumen["efectos"] + 0.1, 1))
                actualizar_volumenes()
   
    return {"accion": "opciones"}

def actualizar_volumenes():
    pygame.mixer.music.set_volume(niveles_volumen["musica"])
    
    if 'juego' in globals() and juego is not None:
        juego.musica.set_volume(niveles_volumen["musica"])
        juego.sonido_laser.set_volume(niveles_volumen["efectos"])
        juego.sonido_explosion.set_volume(niveles_volumen["efectos"])

def iniciar_cuenta_atras():
    for cuenta in range(3, 0, -1):
        pantalla.fill(GRIS_OSCURO)
        texto_cuenta = fuente_grande.render(str(cuenta), True, BLANCO)
        rect_texto = texto_cuenta.get_rect(center=(ancho_pantalla//2, alto_pantalla//2))
        pantalla.blit(texto_cuenta, rect_texto)
        pygame.display.flip()
        pygame.time.delay(1000)

class JugadorMulti(Player):
    def __init__(self, pos, constraint, speed, es_jugador_uno=True):
        super().__init__(pos, constraint, speed)
        self.es_jugador_uno = es_jugador_uno
        if es_jugador_uno:
            self.tecla_izquierda = pygame.K_LEFT
            self.tecla_derecha = pygame.K_RIGHT
            self.tecla_disparo = pygame.K_SPACE
        else:
            self.tecla_izquierda = pygame.K_a
            self.tecla_derecha = pygame.K_d
            self.tecla_disparo = pygame.K_w
    
    def input_jugador(self):
        keys = pygame.key.get_pressed()
        
        if keys[self.tecla_izquierda]:
            self.rect.x -= self.speed
        elif keys[self.tecla_derecha]:
            self.rect.x += self.speed
            
        if keys[self.tecla_disparo] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
    
    def update(self):
        self.input_jugador()
        self.constraint()
        self.recharge()
        self.lasers.update()

class Juego:
    def __init__(self, modo="individual"):
        self.modo = modo
        self.game_over_active = False
        self.victoria_active = False
        
        if modo == "individual":
            jugador_sprite = Player((ancho_pantalla / 2, alto_pantalla - 10), ancho_pantalla, 5)
            self.jugador = pygame.sprite.GroupSingle(jugador_sprite)
            self.jugador2 = None
        else:
            jugador1_sprite = JugadorMulti((ancho_pantalla / 3, alto_pantalla - 10), ancho_pantalla, 5, True)
            self.jugador = pygame.sprite.GroupSingle(jugador1_sprite)
            
            jugador2_sprite = JugadorMulti((ancho_pantalla * 2/3, alto_pantalla - 10), ancho_pantalla, 5, False)
            self.jugador2 = pygame.sprite.GroupSingle(jugador2_sprite)

        self.vidas = 3
        self.superficie_vida = pygame.image.load(get_resource_path('graphics/player.png')).convert_alpha()
        self.pos_x_inicial_vida = ancho_pantalla - (self.superficie_vida.get_size()[0] * 2 + 20)
        self.puntuacion = 0
        self.puntuacion_maxima = cargar_puntuacion_maxima()
        self.fuente = pygame.font.Font(get_resource_path('font/Pixeled.ttf'), 20)

        self.forma = obstacle.shape
        self.tamaño_bloque = 6
        self.bloques = pygame.sprite.Group()
        self.cantidad_obstaculos = 4
        self.posiciones_x_obstaculos = [num * (ancho_pantalla / self.cantidad_obstaculos) for num in range(self.cantidad_obstaculos)]
        self.crear_multiples_obstaculos(*self.posiciones_x_obstaculos, x_inicio=ancho_pantalla / 15, y_inicio=alto_pantalla - 120)

        self.aliens = pygame.sprite.Group()
        self.lasers_aliens = pygame.sprite.Group()
        self.configurar_aliens(filas=6, cols=8)
        self.direccion_alien = 1

        self.extra = pygame.sprite.GroupSingle()
        self.tiempo_aparicion_extra = randint(40, 80)

        pygame.mixer.init()
        self.musica = pygame.mixer.Sound(get_resource_path('audio/music.wav'))
        self.sonido_laser = pygame.mixer.Sound(get_resource_path('audio/laser.wav'))
        self.sonido_explosion = pygame.mixer.Sound(get_resource_path('audio/explosion.wav'))
        
        self.musica.set_volume(niveles_volumen["musica"])
        self.sonido_laser.set_volume(niveles_volumen["efectos"])
        self.sonido_explosion.set_volume(niveles_volumen["efectos"])
        self.musica.play(loops=-1)

    def crear_obstaculo(self, x_inicio, y_inicio, offset_x):
        for indice_fila, fila in enumerate(self.forma):
            for indice_col, col in enumerate(fila):
                if col == 'x':
                    x = x_inicio + indice_col * self.tamaño_bloque + offset_x
                    y = y_inicio + indice_fila * self.tamaño_bloque
                    bloque = obstacle.Block(self.tamaño_bloque, ROJO, x, y)
                    self.bloques.add(bloque)

    def crear_multiples_obstaculos(self, *offset, x_inicio, y_inicio):
        for offset_x in offset:
            self.crear_obstaculo(x_inicio, y_inicio, offset_x)

    def configurar_aliens(self, filas, cols, distancia_x=60, distancia_y=48, offset_x=70, offset_y=100):
        offset_x = (ancho_pantalla - (cols * distancia_x)) // 2
        
        for indice_fila, fila in enumerate(range(filas)):
            for indice_col, col in enumerate(range(cols)):
                x = indice_col * distancia_x + offset_x
                y = indice_fila * distancia_y + offset_y
                
                if indice_fila == 0: sprite_alien = Alien('yellow', x, y)
                elif 1 <= indice_fila <= 2: sprite_alien = Alien('green', x, y)
                else: sprite_alien = Alien('red', x, y)
                self.aliens.add(sprite_alien)

    def verificar_posicion_aliens(self):
        todos_aliens = self.aliens.sprites()
        for alien in todos_aliens:
            if alien.rect.right >= ancho_pantalla:
                self.direccion_alien = -1
                self.mover_aliens_abajo(2)
            elif alien.rect.left <= 0:
                self.direccion_alien = 1
                self.mover_aliens_abajo(2)

    def mover_aliens_abajo(self, distancia):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distancia

    def disparo_alien(self):
        if self.aliens.sprites():
            aliens_por_columna = {}
            for alien in self.aliens:
                col = alien.rect.centerx
                if col not in aliens_por_columna or alien.rect.bottom > aliens_por_columna[col].rect.bottom:
                    aliens_por_columna[col] = alien
            
            if aliens_por_columna:
                alien_disparador = choice(list(aliens_por_columna.values()))
                laser_sprite = Laser(alien_disparador.rect.center, 6, alto_pantalla)
                self.lasers_aliens.add(laser_sprite)
                self.sonido_laser.play()

    def temporizador_alien_extra(self):
        self.tiempo_aparicion_extra -= 1
        if self.tiempo_aparicion_extra <= 0:
            self.extra.add(Extra(choice(['right', 'left']), ancho_pantalla))
            self.tiempo_aparicion_extra = randint(400, 800)

    def verificar_colisiones_laser_jugador(self, sprite_jugador):
        if sprite_jugador.lasers:
            for laser in sprite_jugador.lasers:
                if pygame.sprite.spritecollide(laser, self.bloques, True):
                    laser.kill()
                
                aliens_golpeados = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_golpeados:
                    for alien in aliens_golpeados:
                        self.puntuacion += alien.value
                    laser.kill()
                    self.sonido_explosion.play()
                
                if pygame.sprite.spritecollide(laser, self.extra, True):
                    self.puntuacion += 500
                    laser.kill()

    def verificar_colisiones(self):
        self.verificar_colisiones_laser_jugador(self.jugador.sprite)
        
        if self.jugador2:
            self.verificar_colisiones_laser_jugador(self.jugador2.sprite)

        if self.lasers_aliens:
            for laser in self.lasers_aliens:
                if pygame.sprite.spritecollide(laser, self.bloques, True):
                    laser.kill()

                if pygame.sprite.spritecollide(laser, self.jugador, False):
                    laser.kill()
                    self.vidas -= 1
                    if self.vidas <= 0:
                        self.game_over_active = True
                        self.musica.stop()
                
                if self.jugador2 and pygame.sprite.spritecollide(laser, self.jugador2, False):
                    laser.kill()
                    self.vidas -= 1
                    if self.vidas <= 0:
                        self.game_over_active = True
                        self.musica.stop()

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= alto_pantalla - 50:
                self.game_over_active = True
                self.musica.stop()
                break

        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.bloques, True)

                if pygame.sprite.spritecollide(alien, self.jugador, False):
                    self.game_over_active = True
                    self.musica.stop()
                
                if self.jugador2 and pygame.sprite.spritecollide(alien, self.jugador2, False):
                    self.game_over_active = True
                    self.musica.stop()
    
    def detener_todos_sonidos(self):
        self.musica.stop()
        self.sonido_laser.stop()
        self.sonido_explosion.stop()
        self.lasers_aliens.empty()
        if self.jugador:
            self.jugador.sprite.lasers.empty()
        if self.jugador2:
            self.jugador2.sprite.lasers.empty()

    def mostrar_game_over(self, pantalla):
        self.detener_todos_sonidos()
        
        if self.puntuacion > self.puntuacion_maxima:
            guardar_puntuacion_maxima(self.puntuacion)
            self.puntuacion_maxima = self.puntuacion
            
        s = pygame.Surface((ancho_pantalla, alto_pantalla))
        s.set_alpha(180)
        s.fill((0, 0, 0))
        pantalla.blit(s, (0, 0))
        
        texto_game_over = fuente_grande.render('GAME OVER', True, ROJO)
        rect_game_over = texto_game_over.get_rect(center=(ancho_pantalla//2, alto_pantalla//2 - 50))
        pantalla.blit(texto_game_over, rect_game_over)
        
        texto_puntuacion = fuente.render(f'Puntuacion: {self.puntuacion}', True, BLANCO)
        rect_puntuacion = texto_puntuacion.get_rect(center=(ancho_pantalla//2, alto_pantalla//2))
        pantalla.blit(texto_puntuacion, rect_puntuacion)
        
        if self.puntuacion >= self.puntuacion_maxima:
            texto_record = fuente.render('Nueva puntuacion maxima!', True, VERDE)
            rect_record = texto_record.get_rect(center=(ancho_pantalla//2, alto_pantalla//2 + 40))
            pantalla.blit(texto_record, rect_record)

        boton_menu = Boton("Volver al Menu", 250, 50, ((ancho_pantalla - 250)//2, alto_pantalla//2 + 100), fuente)
        boton_menu.dibujar(pantalla)
        
        pos_raton = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if boton_menu.rect.collidepoint(pos_raton):
                    return True
        
        return False

    def mostrar_victoria(self, pantalla):
        if not self.aliens.sprites():
            self.detener_todos_sonidos()
            
            if not self.victoria_active:
                self.victoria_active = True
            
            if self.puntuacion > self.puntuacion_maxima:
                guardar_puntuacion_maxima(self.puntuacion)
                self.puntuacion_maxima = self.puntuacion
            
            s = pygame.Surface((ancho_pantalla, alto_pantalla))
            s.set_alpha(180)
            s.fill((0, 0, 0))
            pantalla.blit(s, (0, 0))
            
            texto_victoria = fuente_grande.render('HAS GANADO!', True, VERDE)
            rect_victoria = texto_victoria.get_rect(center=(ancho_pantalla//2, alto_pantalla//2 - 50))
            pantalla.blit(texto_victoria, rect_victoria)
            
            texto_puntuacion = fuente.render(f'Puntuacion: {self.puntuacion}', True, BLANCO)
            rect_puntuacion = texto_puntuacion.get_rect(center=(ancho_pantalla//2, alto_pantalla//2))
            pantalla.blit(texto_puntuacion, rect_puntuacion)
            
            if self.puntuacion >= self.puntuacion_maxima:
                texto_record = fuente.render('Nueva puntuacion maxima!', True, VERDE)
                rect_record = texto_record.get_rect(center=(ancho_pantalla//2, alto_pantalla//2 + 40))
                pantalla.blit(texto_record, rect_record)
            
            boton_menu = Boton("Volver al Menu", 250, 50, ((ancho_pantalla - 250)//2, alto_pantalla//2 + 100), fuente)
            boton_menu.dibujar(pantalla)
            
            pos_raton = pygame.mouse.get_pos()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if boton_menu.rect.collidepoint(pos_raton):
                        return True
        
        return False

    def mostrar_vidas(self):
        for vida in range(self.vidas - 1):
            x = self.pos_x_inicial_vida + (vida * (self.superficie_vida.get_size()[0] + 10))
            pantalla.blit(self.superficie_vida, (x, 8))

    def mostrar_puntuacion(self):
        superficie_puntuacion = self.fuente.render(f'Puntos: {self.puntuacion}', False, 'white')
        rect_puntuacion = superficie_puntuacion.get_rect(topleft=(10, 8))
        pantalla.blit(superficie_puntuacion, rect_puntuacion)
        
        superficie_max = self.fuente.render(f'Max: {self.puntuacion_maxima}', False, 'white')
        rect_max = superficie_max.get_rect(midtop=(ancho_pantalla // 2, 8))
        pantalla.blit(superficie_max, rect_max)

    def ejecutar(self):
        if self.game_over_active:
            return self.mostrar_game_over(pantalla)
        
        if not self.aliens.sprites() and not self.victoria_active:
            self.victoria_active = True
            
        if self.victoria_active:
            return self.mostrar_victoria(pantalla)
        
        self.jugador.update()
        
        if self.jugador2:
            self.jugador2.update()
        
        self.lasers_aliens.update()
        self.extra.update()
        
        self.aliens.update(self.direccion_alien)
        self.verificar_posicion_aliens()
        self.temporizador_alien_extra()
        self.verificar_colisiones()
        
        self.jugador.sprite.lasers.draw(pantalla)
        self.jugador.draw(pantalla)
        
        if self.jugador2:
            self.jugador2.sprite.lasers.draw(pantalla)
            self.jugador2.draw(pantalla)
        
        self.bloques.draw(pantalla)
        self.aliens.draw(pantalla)
        self.lasers_aliens.draw(pantalla)
        self.extra.draw(pantalla)
        self.mostrar_vidas()
        self.mostrar_puntuacion()
        
        if not self.aliens.sprites() and not self.victoria_active:
            self.victoria_active = True
        
        return False

if __name__ == '__main__':
    pygame.init()
    ancho_pantalla = 600
    alto_pantalla = 600
    pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
    pygame.display.set_caption("Space Invaders")
    reloj = pygame.time.Clock()
    fuente = pygame.font.Font(get_resource_path('font/Pixeled.ttf'), 16)
    fuente_grande = pygame.font.Font(get_resource_path('font/Pixeled.ttf'), 32)
    puntuacion_maxima = cargar_puntuacion_maxima()
    
    estado_juego = {"accion": "menu", "modo": "individual"}
    juego = None

    DISPARO_ALIEN = pygame.USEREVENT + 1
    pygame.time.set_timer(DISPARO_ALIEN, 800)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == DISPARO_ALIEN and estado_juego["accion"] == "jugar" and juego:
                juego.disparo_alien()
                
        if estado_juego["accion"] == "menu":
            estado_juego = mostrar_menu()
            
            if estado_juego["accion"] == "jugar":
                juego = Juego(modo=estado_juego["modo"])
        
        elif estado_juego["accion"] == "opciones":
            estado_juego = mostrar_opciones()
        
        elif estado_juego["accion"] == "jugar":
            pantalla.fill(GRIS_OSCURO)
            if juego.ejecutar():
                juego.musica.stop()
                estado_juego = {"accion": "menu"}
            
        pygame.display.flip()
        reloj.tick(60)