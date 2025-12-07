import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Part 1: Foundations of Physical AI',
      items: [
        {type: 'doc', id: 'introduction'},
        {type: 'doc', id: 'chapter1'},
        {type: 'doc', id: 'chapter2'},
        {type: 'doc', id: 'physical-ai-course/module-1-ros2'},
        {type: 'doc', id: 'chapter4'},
        {type: 'doc', id: 'chapter5'},
        {type: 'doc', id: 'chapter6'},
      ],
    },
    {
      type: 'category',
      label: 'Part 2: Building Humanoid Robots',
      items: [
        {type: 'doc', id: 'chapter7'},
        {type: 'doc', id: 'chapter8'},
        {type: 'doc', id: 'chapter9'},
        {type: 'doc', id: 'chapter10'},
      ],
    },
    {
      type: 'category',
      label: 'Part 3: The AI Brain of the Robot',
      items: [
        {type: 'doc', id: 'chapter11'},
        {type: 'doc', id: 'chapter12'},
        {type: 'doc', id: 'chapter13'},
        {type: 'doc', id: 'physical-ai-course/module-3-nvidia-isaac'},
        {type: 'doc', id: 'chapter15'},
      ],
    },
    {
      type: 'category',
      label: 'Part 4: Advanced Topics and Future Directions',
      items: [
        {type: 'doc', id: 'chapter16'},
        {type: 'doc', id: 'chapter17'},
        {type: 'doc', id: 'chapter18'},
        {type: 'doc', id: 'chapter19'},
        {type: 'doc', id: 'chapter20'},
      ],
    },
  ],
};

export default sidebars;
