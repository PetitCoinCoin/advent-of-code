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

def count_increases(data)
  counter = 0
  data.each_with_index {
    |val, idx|
    if idx > 0 and val > data[idx - 1]
      counter += 1
    end
  }
  return counter
end

if __FILE__ == $0
    args = parse_args
    t = Time.now
    data = nil
    File.open("#{File.dirname($0)}/inputs/#{File.basename($0, ".*")}.txt", "r") do |f|
      data = f.read.split("\n").map { |x| x.to_i }
    end

    if args.part == "2"
      data = (0..data.length - 3).map {
        |idx|
        data[idx] + data[idx + 1] + data[idx + 2]
      }
    end

    puts count_increases(data)
    puts Time.now - t
end
