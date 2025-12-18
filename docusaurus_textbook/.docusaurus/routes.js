import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', '5ff'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', '5ba'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', 'a2b'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', 'c3c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', '156'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '88c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '000'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', '0e0'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', '69f'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', 'fd4'),
            routes: [
              {
                path: '/docs/advanced-ai-control/module-5-advanced-ai',
                component: ComponentCreator('/docs/advanced-ai-control/module-5-advanced-ai', 'e09'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/appendix/glossary',
                component: ComponentCreator('/docs/appendix/glossary', '16e'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/appendix/references',
                component: ComponentCreator('/docs/appendix/references', 'bd3'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/appendix/resources',
                component: ComponentCreator('/docs/appendix/resources', '84e'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/hardware-basics/module-3-hardware',
                component: ComponentCreator('/docs/hardware-basics/module-3-hardware', '822'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/humanoid-design/module-6-humanoid-design',
                component: ComponentCreator('/docs/humanoid-design/module-6-humanoid-design', '6be'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/intro',
                component: ComponentCreator('/docs/intro', '61d'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/introduction/intro',
                component: ComponentCreator('/docs/introduction/intro', '61f'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ros2-foundations/module-1-ros2',
                component: ComponentCreator('/docs/ros2-foundations/module-1-ros2', 'dc0'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ros2-foundations/ros2-hands-on',
                component: ComponentCreator('/docs/ros2-foundations/ros2-hands-on', '6fd'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/simulation/digital-twins',
                component: ComponentCreator('/docs/simulation/digital-twins', '2dd'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/simulation/gazebo-unity',
                component: ComponentCreator('/docs/simulation/gazebo-unity', '47c'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/simulation/module-2-simulation',
                component: ComponentCreator('/docs/simulation/module-2-simulation', '224'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/vla-systems/module-4-vla-foundations',
                component: ComponentCreator('/docs/vla-systems/module-4-vla-foundations', '685'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/vla-systems/vla-action',
                component: ComponentCreator('/docs/vla-systems/vla-action', 'b08'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/vla-systems/vla-hands-on-basic',
                component: ComponentCreator('/docs/vla-systems/vla-hands-on-basic', '21c'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/vla-systems/vla-language',
                component: ComponentCreator('/docs/vla-systems/vla-language', '8c1'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/vla-systems/vla-vision',
                component: ComponentCreator('/docs/vla-systems/vla-vision', '596'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', '2e1'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
