'use client';

import { Menu, Card, Avatar, Progress, Dropdown } from 'antd';
import { UserOutlined, DownOutlined } from '@ant-design/icons';

const user = {
    name: 'DeltaHacks',
    email: 'uw-sadge@gmail.com',
};

const { Meta } = Card;


const HomePage = () => {
    return (
        <main className='flex bg-gray-50 h-[100vh]'>
            <div className='flex-1 px-20 py-10'>
                {/* Two Column Layout */}
                <div className='grid grid-cols-3 gap-10'>
                    <div className='col-span-2'>
                        <div className='bg-white rounded-xl shadow-md p-8'>
                            <h1 className='text-4xl font-bold text-gray-900 mb-6'>Welcome, {user.name}! 🎉</h1>
                            <p className='text-lg text-gray-600 mb-8'>Unlock Your Potential, Discover New Opportunities.</p>

                            <div>
                                <Menu mode="horizontal" defaultSelectedKeys={['urgent']} className="border-b mb-6">
                                    <Menu.Item key="urgent">AAAAA</Menu.Item>
                                    <Menu.Item key="all">BBBBB</Menu.Item>
                                </Menu>
                                <div className='space-y-4'>
                     
                                </div>
                            </div>
                        </div>

                        <div className='bg-white rounded-xl shadow-md p-8 mt-10'>

                        </div>

                    </div>

                    {/* Right Column */}
                    <div className='bg-white rounded-xl shadow-md p-8'>
                        {/* User Profile Section */}
                        <Card bordered={false} className='rounded-xl'>
                            <Meta
                                avatar={<Avatar size="large" style={{ backgroundColor: '#3182ce' }}>{user.name.charAt(0)}</Avatar>}
                                title={<h3 className='text-2xl font-semibold'>{user.name}</h3>}
                                description={
                                    <div>
                                        <p className='text-lg'>{user.email}</p>
                                        <div className='mt-4'>
                                            <p className='text-sm font-semibold text-gray-600 mb-2'>Profile Progress</p>
                                            <Progress percent={75} status="active" showInfo={false} strokeColor={{
                                                '0%': '#3182ce',
                                                '100%': '#63b3ed',
                                            }} />
                                        </div>
                                    </div>
                                }
                                className='mt-4'
                            />
                        </Card>
                    </div>
                </div>
            </div>
        </main>
    )
}

export default HomePage;
