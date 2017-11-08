require('triangle')
function love.load()
  columns = 12
  rows = 6
  size = 10
  scale = 5

  mouse_x = 0
  mouse_y = 0
  last_clicked_cell = ''

  --Create table for triangle
  triangles = {}
  for y = 1, rows do
    for x = 1, columns do
      --Insert new triangles into table
      table.insert(triangles, Triangle:new({x=x, y=y, size=size}))
    end
  end
end

function determine_click()
  if mouse_x < 60 and mouse_x > 0 then
    if mouse_y < 60 and mouse_y > 0 then
      column = (mouse_x / 10)
      row = (mouse_y / 10)
      column_remainder = column % 1
      row_remainder = row % 1
      index = (math.floor(column) * 2) + (math.floor(row) * columns) + 1
      if row_remainder < column_remainder then
        index = index + 1
      end
      last_clicked_cell = triangles[index].name
      triangles[index].time_clicked = os.time()
    end
  end
end

function love.update(dt)
  if love.mouse.isDown(1) then
    mouse_x, mouse_y = love.mouse.getPosition()
    mouse_x = (mouse_x - x_offset) / scale
    mouse_y = (mouse_y - y_offset)/ scale
    determine_click()
  end
  if love.keyboard.isDown('up') then
    scale = scale + 10 * dt
  elseif love.keyboard.isDown('down') then
    scale = scale - 10 * dt
  end
  x_offset = (love.graphics.getWidth() / 2) - (size * columns * (scale /4))
  y_offset = (love.graphics.getHeight() / 2) - (size * rows * (scale / 2))
end

function love.draw()
  --Before drawing make sure objects are appropriately centered
  love.graphics.print("Last click at X " .. mouse_x .. " Y " .. mouse_y, 10, 10)
  love.graphics.print("Last clicked cell " .. last_clicked_cell, 10, 30)
  love.graphics.translate(x_offset, y_offset)
  love.graphics.scale(scale, scale)
  for _, triangle in ipairs(triangles) do
    --draw each triangle
    triangle:draw(scale)
  end
end
