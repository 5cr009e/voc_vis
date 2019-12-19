from xml.etree import ElementTree as ET
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
import click
import json


with open("config.json", "r") as config_file:
    config = json.loads(config_file.read())


def parse_rect(tree):
    """Parsing rectangles from VOC format xml file,
       referenced from https://www.codeleading.com/article/4477644963/

    Args:
        tree (tree): tree of xml file

    Returns:
        [dict]: [dictionary of each object]
    """
    objects = []
    for obj in tree.findall('object'):
        obj_struct = {}
        obj_struct['name'] = obj.find('name').text
        obj_struct['difficult'] = int(obj.find('difficult').text)
        bbox = obj.find('bndbox')
        obj_struct['bbox'] = [int(bbox.find('xmin').text),
                              int(bbox.find('ymin').text),
                              int(bbox.find('xmax').text),
                              int(bbox.find('ymax').text)]
        objects.append(obj_struct)
    return objects


def draw_rect(ax, objs, colormap=config['colormap']):
    paches, colors = [], []
    for obj in objs:
        xmin, ymin, xmax, ymax = obj['bbox']
        paches.append(Rectangle((xmin, ymin), xmax - xmin, ymax - ymin))
        colors.append(colormap[obj['name'] if obj['name'] in colormap.keys()
                      else 'default'])
    pc = PatchCollection(paches, facecolor='None', alpha=0.7, edgecolor=colors,
                         linewidth=2)
    ax.add_collection(pc)


@click.command()
@click.option('--img_id', default=config['img_id'], help='Sample ID.')
@click.option('--ir_img_path', default=config['ir_img_path']+'/',
              help='IR image path.')
@click.option('--ir_anno_path', default=config['ir_anno_path']+'/',
              help='IR annotation path.')
@click.option('--rgb_img_path', default=config['rgb_img_path']+'/',
              help='RGB image path.')
@click.option('--rgb_anno_path', default=config['rgb_anno_path']+'/',
              help='RGB annotation path.')
def plot_rect_cli(img_id, ir_img_path='./', ir_anno_path='./',
                  rgb_img_path='./', rgb_anno_path='./'):
    fig, ax = plt.subplots(2)
    plot_rect(ax, img_id, ir_img_path, ir_anno_path,
              rgb_img_path, rgb_anno_path)


def plot_rect(ax, img_id, ir_img_path='./', ir_anno_path='./',
              rgb_img_path='./', rgb_anno_path='./'):
    """Plot the image and annotation for a single sample

    Args:
        img_id ([type]): image id
        ir_img_path (str, optional): IR image path.
        ir_anno_path (str, optional): IR annotation path.
        rgb_img_path (str, optional): RGB image path.
        rgb_anno_path (str, optional): RGB annotation path.
    """
    def plot_single_img(ax, img_path, xml_path):
        tree = ET.parse(xml_path)
        img_mat = mpl.image.imread(img_path)
        ax.imshow(img_mat)
        draw_rect(ax, parse_rect(tree), config['colormap'])

    plot_single_img(ax[0], rgb_img_path +
                    'IR_{img_id}.jpg'.format(img_id=img_id),
                    rgb_anno_path+'IR_{img_id}.xml'.format(img_id=img_id))
    plot_single_img(ax[1], ir_img_path +
                    'IR_{img_id}HongWai.jpg'.format(img_id=img_id),
                    ir_anno_path +
                    'IR_{img_id}HongWai.xml'.format(img_id=img_id))
    plt.show(block=True)


if __name__ == '__main__':
    plot_rect_cli()
