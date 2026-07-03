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

def parse_input(raw)
  blocks = raw.split("\n\n")
  numbers = blocks[0].split(",").map { |x| x.to_i }
  grids = blocks[1..].map {
    |grid|
    Grid.new(
      grid.split("\n").map {
        |row|
        row.scan(/\d+/).map { |x| x.to_i }
      }
    )
  }
  return numbers, grids
end

class Grid
  attr_accessor :rows

  def initialize(rows)
    @rows = rows
  end

  def is_winning(numbers)
    return has_full_row(numbers) || has_full_column(numbers)
  end

  def unmarked(numbers)
    return @rows.flatten - numbers    
  end

  def has_full_column(numbers)
    (0..@rows.length - 1).any? {
      |idx|
      (@rows.map { |row| row[idx] } - numbers).empty?
    }
  end

  def has_full_row(numbers)
    @rows.any? {
      |row|
      (row - numbers).empty?
    }
  end
end

if __FILE__ == $0
    args = parse_args
    t = Time.now
    numbers = nil
    grids = nil
    File.open("#{File.dirname($0)}/inputs/#{File.basename($0, ".*")}.txt", "r") do |f|
      numbers, grids = parse_input(f.read)
    end
    if args.part == "1"
      numbers.each_with_index {
        |n, i|
        done = false
        grids.each {
          |grid|
          if grid.is_winning(numbers[..i])
            puts n * grid.unmarked(numbers[..i]).sum
            done = true
            break
          end
        }
        break if done
      }
    else
      numbers.each_with_index {
        |n, i|
        done = false
        if grids.length > 1
          grids.filter! { |grid| not grid.is_winning(numbers[..i]) }
        else
          grid = grids[0]
          if grid.is_winning(numbers[..i])
            puts n * grid.unmarked(numbers[..i]).sum
            done = true
          end
        end
        break if done
      }
    end
    puts Time.now - t
end
