import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docsSidebar: [
    'intro',
    'installation',
    'quick-start',
    {
      type: 'category',
      label: 'API Reference',
      items: [
        'api/provider',
        'api/contract',
        'api/types',
        'api/errors',
        'api/utils',
      ],
    },
  ],
};

export default sidebars;
