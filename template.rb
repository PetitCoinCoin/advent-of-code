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

if __FILE__ == $0
    args = parse_args
    t = Time.now
    data = nil
    File.open("#{File.dirname($0)}/inputs/#{File.basename($0, ".*")}.txt", "r") do |f|
      data = f.read.split("\n")
    end
    if args.part == "1"
      puts data
    else
        raise "Solve part 1 first ;)"
    end
    puts Time.now - t
end
