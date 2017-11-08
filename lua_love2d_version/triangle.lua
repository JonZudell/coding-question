Triangle = {}

Shader = love.graphics.newShader[[
extern int current_time;
extern int time_clicked;
vec4 effect(vec4 color, Image texture, vec2 texture_coords, vec2 screen_coords) {
  float diff = clamp((current_time - time_clicked) * 200,0,1000);
  float inverse = (1000 - diff) / 1000.0;
  diff = diff / 1000.0;
  vec4 pixel = vec4(0.5,0.5,0,1);
  pixel.r += inverse;
  pixel.g = .5;
  pixel.b += diff;
  return pixel;
}
]]

function Triangle:new(o)
  --object creation
  o = o
  setmetatable(o, self)
  self.__index = self
  --openGL expects vertices to appear as follows
  --vertices = {v1x, v1y, v2x, v2y, ...}
  --x_offset because collumn 2 is above column 1
  local x_offset = math.floor((o.x - 1) / 2)
  if o.x % 2 == 0 then
    o.vertices = {(o.x - 2 - x_offset) * o.size,(o.y - 1) * o.size,
                  (o.x - 1 - x_offset) * o.size, (o.y - 1) * o.size,
                  (o.x - 1 - x_offset) * o.size, o.y * o.size}
  else
    o.vertices = {(o.x - 1 - x_offset) * o.size,(o.y - 1) * o.size,
                  (o.x - 1 - x_offset) * o.size, o.y  * o.size,
                  (o.x - x_offset) * o.size, o.y * o.size}
  end
  o.x_centroid = (o.vertices[1] + o.vertices[3] + o.vertices[5]) / 3
  o.y_centroid = (o.vertices[2] + o.vertices[4] + o.vertices[6]) / 3
  o.name = string.char(64 + o.y) .. o.x
  o.text = love.graphics.newText(love.graphics.getFont(),o.name)
  o.time_clicked = 0
  return o
end

function Triangle:draw()
  love.graphics.setShader(Shader)
  Shader:send('time_clicked', self.time_clicked)
  Shader:send('current_time', os.time())
  love.graphics.polygon('fill', self.vertices)
  love.graphics.setShader()
  love.graphics.setColor(0,0,0)
  love.graphics.polygon('line', self.vertices)
  love.graphics.setColor(255,255,255)
  love.graphics.draw(self.text,
                     self.x_centroid - (self.text:getWidth() / (10)),
                     self.y_centroid - (self.text:getHeight() / (10)),
                     0, .2, .2)
end
