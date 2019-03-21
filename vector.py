import pygame
import tank
pygame.init()
white = (255,255,255)
entity = []
window = pygame.display.set_mode((800,600))
pygame.display.set_caption("Tank")

exit =False
while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            temp = tank.Bullet(x,y,-60)
            entity.append(temp)
            print("shoot")
    window.fill(white)
    for item in entity:
        item.update()
    for item in entity:
        item.draw(window)
    pygame.display.update()
pygame.quit()
quit