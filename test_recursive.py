import sys
import os
sys.path.insert(0, 'src')

from functions import generate_pages_recursive

# Clean up test output directory if it exists
import shutil
if os.path.exists('test_output'):
    shutil.rmtree('test_output')

# Run the recursive generation
try:
    generate_pages_recursive('test_content', 'template.html', 'test_output')
    print("✓ Function completed successfully")
    
    # Check what was generated
    print("\nGenerated files:")
    for root, dirs, files in os.walk('test_output'):
        for file in files:
            filepath = os.path.join(root, file)
            print(f"  {filepath}")
            if file == 'index.html':
                with open(filepath, 'r') as f:
                    content = f.read()
                    # Check if title was extracted
                    if '<title>' in content and '</title>' in content:
                        title = content.split('<title>')[1].split('</title>')[0]
                        print(f"    Title: {title}")
                    # Check if content was generated
                    if '<article>' in content:
                        print(f"    ✓ Has article content")
                    else:
                        print(f"    ✗ Missing article content")
                        
except Exception as e:
    print(f"✗ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
