require 'test/unit'
require './omegastar'

$logger.level = Logger::WARN

class BisectTests < Test::Unit::TestCase
  def test_succeeding_with_full_items_raises_standard_error
    assert_raise(StandardError.new "Command succeeded with full items") do
      run_bisect(lambda { |items| true }, [1, 2, 3])
    end
  end

  def test_failing_with_empty_items_raises_standard_error
    assert_raise(StandardError.new "Command failed with empty items") do
      run_bisect(lambda { |items| false }, [])
    end
  end

  def test_bisect_one
    def command(items)
      !(items.include? 2)
    end
    
    result = run_bisect(method(:command), (1..5).to_a)
    assert_equal([2], result)
  end

  def test_bisect_two
    def command(items)
      return !(items.include?(1) && items.include?(5))
    end

    result = run_bisect(method(:command), (1..5).to_a)
    assert_equal([1, 5], result)
  end

  def test_bisect_three
    def command(items)
      return !(items.include?(1) && items.include?(3) && items.include?(5))
    end

    result = run_bisect(method(:command), (1..5).to_a)
    assert_equal([1, 3, 5], result)
  end

  def test_bisect_n
    $n_steps = 0
    def command(items)
      $n_steps += 1
      return !(items.include?(-5) && items.include?(1) && items.include?(3) && items.include?(5))
    end

    result = run_bisect(method(:command), (-1_000_000..1_000_000).to_a)
    assert_equal([-5, 1, 3, 5], result)
    assert_equal($n_steps, 69)
  end
end
