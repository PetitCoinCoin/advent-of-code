require 'optparse'
require 'ostruct'

def parse_args
  args = OpenStruct.new
  OptionParser.new do |arg|
    arg.on('-p', '--part PART', 'The part you\'re solving') { |a| args.part = a }
  end.parse!
  if not args.part
    raise "Which part are you solving?"
  end
  return args
end

def parse_input(line)
  movement = OpenStruct.new
  value = line.scan(/\d+/)[0].to_i
  if line.include? "forward"
    movement.x = value
    movement.y = 0
  else
    movement.x = 0
    movement.y = line.include?("down") ? value : -value
  end
  return movement
end

if __FILE__ == $0
    args = parse_args
    t = Time.now
    data = nil
    File.open("#{File.dirname($0)}/inputs/#{File.basename($0, ".*")}.txt", "r") do |f|
      data = f.read.split("\n").map{ |line| parse_input(line)}
    end
    pos = OpenStruct.new({ x: 0, y: 0 })
    if args.part == "1"
      data.each {
        |mvt|
        pos.x += mvt.x
        pos.y += mvt.y
      }
    else
      aim = 0
      data.each {
        |mvt|
        pos.x += mvt.x
        pos.y += mvt.x * aim
        aim += mvt.y
      }
    end
    puts pos.x * pos.y
    puts Time.now - t
end
