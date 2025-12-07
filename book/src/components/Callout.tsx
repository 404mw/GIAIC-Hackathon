import React from 'react';
import type {ReactNode} from 'react';

interface Props {
  title: string;
  children: ReactNode;
}

export default function Callout({title, children}: Props): JSX.Element {
  return (
    <div
      style={{
        border: '1px solid #e0e0e0',
        borderRadius: '8px',
        padding: '1rem',
        margin: '1.5rem 0',
      }}>
      <div style={{fontWeight: 'bold', marginBottom: '0.5rem'}}>{title}</div>
      <div>{children}</div>
    </div>
  );
}
