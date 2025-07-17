require 'logger'

$logger = Logger.new($stdout)

def bisect_impl(command, fixed, items, indent="")
  $logger.info("#{indent}step fixed[#{fixed.length}] and items[#{items.length}]")
  while items.length > 1
    $logger.info("#{indent}#{fixed.length + items.length} candidates")
    # Return two halves of the given list. For odd-length lists, the second
    # half will be larger.
    half = items.length / 2
    left = items[0...half]
    right = items[half..]
    if !command.call(fixed + left)
      items = left
      next
    end
    if !command.call(fixed + right)
      items = right
      next
    end
    # We need something from both halves to trigger the failure. Try
    # holding each half fixed and bisecting the other half to reduce the
    # candidates.
    new_right = bisect_impl(command, fixed + left, right, indent + "< ")
    new_left = bisect_impl(command, fixed + new_right, left, indent + "> ")
    return new_left + new_right
  end
  items
end

def run_bisect(command, items)
  $logger.info("Verifying items")
  if command.call(items)
    raise StandardError.new("Command succeeded with full items")
  end
  if !command.call([])
    raise StandardError.new("Command failed with empty items")
  end
  bisect_impl(command, [], items)
end
