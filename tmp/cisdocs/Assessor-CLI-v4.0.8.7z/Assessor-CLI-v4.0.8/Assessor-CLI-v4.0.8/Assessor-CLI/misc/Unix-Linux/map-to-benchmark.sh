#!/bin/bash

map_to_benchmark()
{
        _DISTRO=$1
        _VER=$2

        case $_DISTRO in
                OSX)
                        # -- The following OSX benchmarks are not supported in v4:
                        # OSX 10.5
                        # OSX 10.6
                        # OSX 10.8
                        # OSX 10.9

                        # OSX 10.10
                        if [ `expr $_VER \>= 14.0 \& $_VER \< 15.0` -eq 1 ]
                        then
                                BENCHMARK="CIS_Apple_OSX_10.10_Benchmark_v1.2.0.xml"
                                PROFILE1="Level 1"
                                PROFILE2="Level 2"
                                ARFORXML="-x"
                        fi

                        # OSX 10.11
                        if [ `expr $_VER \>= 15.0 \& $_VER \< 16.0` -eq 1 ]
                        then
                                BENCHMARK="CIS_Apple_OSX_10.11_Benchmark_v1.1.0.xml"
                                PROFILE1="Level 1"
                                PROFILE2="Level 2"
                                ARFORXML="-x"
                        fi

                        # OSX 10.12
                        if [ `expr $_VER \>= 16.0 \& $_VER \< 17.0` -eq 1 ]
                        then
                                BENCHMARK="CIS_Apple_OSX_10.12_Benchmark_v1.0.0.xml"
                                PROFILE1="Level 1"
                                PROFILE2="Level 2"
                                ARFORXML="-x"
                        fi

                        # OSX 10.13
                        if [ `expr $_VER \>= 17.0` -eq 1 ]
                        then
                                BENCHMARK="CIS_Apple_macOS_10.13_Benchmark_v1.0.0.1-xccdf.xml"
                                PROFILE1="Level 1"
                                PROFILE2="Level 2"
                                ARFORXML="-x"
                        fi

                        ;;
                Debian)
                        if [ `expr $_VER \>= 7 \& $_VER \< 8` -eq 1 ]
                        then
                                BENCHMARK="CIS_Debian_Linux_7_Benchmark_v1.0.0-xccdf.xml"
                                PROFILE1="Level 1"
                                PROFILE2="Level 2"
                        fi

                        if [ `expr $_VER \>= 8 \& $_VER \< 9` -eq 1 ]
                        then
                                BENCHMARK="CIS_Debian_Linux_8_Benchmark_v2.0.0.1-xccdf.xml"
                                PROFILE1="Level 1 - Server"
                                PROFILE2="Level 2 - Server"
                        fi

                        if [ `expr $_VER \>= 9` -eq 1 ]
                        then
                                BENCHMARK="CIS_Debian_Linux_9_Benchmark_v1.0.0-xccdf.xml"
                                PROFILE1="Level 1 - Server"
                                PROFILE2="Level 2 - Server"
                        fi

                        ;;
                Ubuntu)
                	# Ubuntu 14.04
                        if [ `expr $_VER == 14.04` -eq 1 ]
                        then
				BENCHMARK="CIS_Ubuntu_Linux_14.04_LTS_Benchmark_v2.0.0-xccdf.xml"
				PROFILE1="Level 1 - Server"
				PROFILE2="Level 2 - Server"
			fi
                        
                        # Ubuntu 16.04
                        if [ `expr $_VER == 16.04` -eq 1 ]
                        then
                                BENCHMARK="CIS_Ubuntu_Linux_16.04_LTS_Benchmark_v1.0.0-xccdf.xml"
                                PROFILE1="Level 1 - Server"
                                PROFILE2="Level 2 - Server"
                        fi
                        
                        # Ubuntu 18.04
                        if [ `expr $_VER == 18.04` -eq 1 ]
                        then
                                BENCHMARK="CIS_Ubuntu_Linux_18.04_LTS_Benchmark_v1.0.0-xccdf.xml"
                                PROFILE1="Level 1 - Server"
                                PROFILE2="Level 2 - Server"
                        fi
			
			;;
                RedHat)
                        # RHEL 5
                        if [ `expr $_VER \>= 5.0 \& $_VER \< 6.0` -eq 1 ]
                        then
                                BENCHMARK="CIS_Red_Hat_Enterprise_Linux_5_Benchmark_v2.2.0-xccdf.xml"
                                PROFILE1="Level 1"
                                PROFILE2="Level 2"
                        fi

                        # RHEL 6
                        if [ `expr $_VER \>= 6.0 \& $_VER \< 7.0` -eq 1 ]
                        then
                                BENCHMARK="CIS_Red_Hat_Enterprise_Linux_6_Benchmark_v2.0.2-xccdf.xml"
                                PROFILE1="Level 1 - ${ROLE}"
                                PROFILE2="Level 2 - ${ROLE}"
                        fi

                        # RHEL 7
                        if [ `expr $_VER \>= 7.0 \& $_VER \< 8.0` -eq 1 ]
                        then
                                BENCHMARK="CIS_Red_Hat_Enterprise_Linux_7_Benchmark_v2.2.0-xccdf.xml"
                                PROFILE1="Level 1 - ${ROLE}"
                                PROFILE2="Level 2 - ${ROLE}"
                        fi

                        ;;
                CentOS)
                	# CentOS 6
			if [ `expr $_VER \>= 6.0 \& $_VER \< 7.0` -eq 1 ]
			then
				BENCHMARK="CIS_CentOS_Linux_6_Benchmark_v2.0.2-xccdf.xml"
				PROFILE1="Level 1 - ${ROLE}"
				PROFILE2="Level 2 - ${ROLE}"
			fi
			
                	# CentOS 7
			if [ `expr $_VER \>= 7.0 \& $_VER \< 8.0` -eq 1 ]
			then
				BENCHMARK="CIS_CentOS_Linux_7_Benchmark_v2.2.0-xccdf.xml"
				PROFILE1="Level 1 - ${ROLE}"
				PROFILE2="Level 2 - ${ROLE}"
			fi
			
                        ;;
                SUSE)
                        # SUSE 12
                        if [ `expr $_VER \>= 12.0 \& $_VER \< 13.0` -eq 1 ]
                        then
                                BENCHMARK="CIS_SUSE_Linux_Enterprise_12_Benchmark_v2.0.0-xccdf.xml"
				PROFILE1="Level 1 - Workstation"
				PROFILE2="Level 2 - Workstation"
                        fi

                        # SUSE 11
                        if [ `expr $_VER \>= 11.0 \& $_VER \< 12.0` -eq 1 ]
                        then
                                BENCHMARK="CIS_SUSE_Linux_Enterprise_11_Benchmark_v2.0.0-xccdf.xml"
                                PROFILE1="Level 1 - Workstation"
                                PROFILE2="Level 2 - Workstation"
                        fi

                        ;;
        esac
}
