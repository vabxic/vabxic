import argparse
import os
import xml.etree.ElementTree as ET


def resize_svg(src_path: str, dest_path: str, size: int):
    try:
        tree = ET.parse(src_path)
        root = tree.getroot()
        # Ensure svg namespace handling
        # Set width/height attributes (use px units)
        root.set('width', f'{size}px')
        root.set('height', f'{size}px')
        # If there's no viewBox, try to infer from width/height
        if 'viewBox' not in root.attrib:
            # some SVGs may have numeric width/height we can copy into viewBox
            w = root.attrib.get('width')
            h = root.attrib.get('height')
            try:
                if w and h:
                    # strip units
                    wv = float(''.join(ch for ch in w if (ch.isdigit() or ch == '.')))
                    hv = float(''.join(ch for ch in h if (ch.isdigit() or ch == '.')))
                    root.set('viewBox', f'0 0 {int(wv)} {int(hv)}')
            except Exception:
                pass

        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        tree.write(dest_path, encoding='utf-8', xml_declaration=True)
        return True, None
    except ET.ParseError as e:
        return False, f'XML parse error: {e}'
    except Exception as e:
        return False, str(e)


def main():
    parser = argparse.ArgumentParser(description='Resize SVG icons by setting width/height attributes')
    parser.add_argument('--icons-dir', default='icons', help='Source icons directory')
    parser.add_argument('--out-dir', default='icons/resized', help='Output directory for resized icons')
    parser.add_argument('--size', type=int, default=48, help='Target square size in pixels')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite original files')
    args = parser.parse_args()

    src_dir = args.icons_dir
    out_dir = args.out_dir
    size = args.size

    if not os.path.isdir(src_dir):
        print(f'Source directory not found: {src_dir}')
        return

    svg_files = [f for f in os.listdir(src_dir) if f.lower().endswith('.svg')]
    if not svg_files:
        print('No SVG files found in', src_dir)
        return

    for fname in svg_files:
        src_path = os.path.join(src_dir, fname)
        if args.overwrite:
            dest_path = src_path
        else:
            dest_path = os.path.join(out_dir, fname)

        ok, err = resize_svg(src_path, dest_path, size)
        if ok:
            print('Resized', fname, '->', dest_path)
        else:
            print('Failed', fname, err)


if __name__ == '__main__':
    main()
