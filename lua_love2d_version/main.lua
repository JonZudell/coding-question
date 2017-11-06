require('triangle')
function love.load()
  columns = 12
  rows = 6
  size = 10
  scale = 5

  --Create table for triangle
  triangles = {}
  for x = 1, columns do
    for y = 1, rows do
      --Insert new triangles into table
      table.insert(triangles, Triangle:new({x=x, y=y, size=size}))
    end
  end
end

function love.update(dt)
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
  love.graphics.translate(x_offset, y_offset)
  love.graphics.scale(scale, scale)
  for _, triangle in ipairs(triangles) do
    --draw each triangle
    triangle:draw(scale)
  end
end
