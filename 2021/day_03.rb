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

def find_rating(binaries, is_co2)
  rating_values = binaries.clone
  idx = 0
  while rating_values.length > 1 do
    val = rating_values.sum { |b| b[idx] } >= rating_values.length.to_f / 2 ? 1 : 0
    if is_co2
      val = (val + 1) % 2
    end
    rating_values.filter! { |item| item[idx] == val}
    idx += 1
  end
  return rating_values[0].map { |x| x.to_s }.sum("").to_i(2)
end

if __FILE__ == $0
    args = parse_args
    t = Time.now
    data = nil
    File.open("#{File.dirname($0)}/inputs/#{File.basename($0, ".*")}.txt", "r") do |f|
      data = f.read.split("\n").map{ |raw| raw.split("").map{ |x| x.to_i }}
    end

    nb_count = data.length
    bit_count = data[0].length
    most_commons = (0..bit_count - 1).map {
      |idx|
      data.sum {|b| b[idx]} >= (nb_count / 2) ? "1" : "0"
    }

    if args.part == "1"
      gamma_rate = most_commons.sum("").to_i(2)
      epsilon_rate = gamma_rate ^ ("1" * bit_count).to_i(2)
      puts gamma_rate * epsilon_rate
    else
      oxygen_generator_rating = find_rating(data, false)
      co2_scrubber_rating = find_rating(data, true)
      puts oxygen_generator_rating * co2_scrubber_rating
    end
    puts Time.now - t
end
